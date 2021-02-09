"""
PrintLabelView.py - manage the view to print QR codes on labels or paper.
"""

from dataclasses import InitVar, dataclass
from io import BufferedReader, BytesIO, DEFAULT_BUFFER_SIZE
from logging import getLogger
from os import remove
from typing import List, Optional

from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Max
from django.http import FileResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
import pyqrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Image

from fpiweb.support.PermissionsManagement import ManageUserPermissions
from fpiweb.constants import \
    QR_LABELS_MAX, \
    QR_LABELS_PER_PAGE, \
    UserInfo

from fpiweb.models import Box
from fpiweb.views import add_navbar_vars

__author__ = 'Travis Risner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "07/22/2020"
# Copyright 2020 by Travis Risner - MIT License

logger = getLogger('fpiweb')

"""
Assuming:
-   letter size paper

    -   portrait orientation

-   1/2 inch outer margin on all sides
-   all measurements in points (1 pt = 1/72 in)
-   3 labels across
-   4 labels down
-   each label has 1/4 in margin on all sides
-   0, 0 of axis is in lower left corner
"""


@dataclass()
class Point:
    """
    Horizontal (x) and vertical (y) coordinate.
    """
    x: int
    y: int


LABEL_SIZE: Point = Point(144, 144)  # 2 in x 2 in
LABEL_MARGIN: Point = Point(18, 18)  # 1/4 in x 1/4 in
BACKGROUND_SIZE: Point = Point(
    LABEL_SIZE.x + (LABEL_MARGIN.x * 2),
    LABEL_SIZE.y + (LABEL_MARGIN.y * 2)
)
PAGE_OFFSET: Point = Point(36, 36)  # 1/2 in x 1/2 in
TITLE_ADJUSTMENT: Point = Point(+20, -9)


@dataclass
class LabelPosition:
    """
    Container for measurements for one label.

    All measurements are in points.
    x denotes horizontal measurement
    y denotes vertical
    origin is in lower left corner
    label is assumed to be 2 in x 2 in ( 144 pt x 144 pt)
    """
    page_offset: InitVar[Point]
    lower_left_offset: Point = Point(0, 0)
    lower_right_offset: Point = Point(0, 0)
    upper_left_offset: Point = Point(0, 0)
    upper_right_offset: Point = Point(0, 0)
    offset_on_page: Point = Point(0, 0)
    image_start: Point = Point(0, 0)
    title_start: Point = Point(0, 0)

    def __post_init__(self, page_offset: Point):
        """
        Adjust offsets based on offset_on_page.

        :param page_offset: offset (in points) from the lower left corner
        :return:
        """
        self.offset_on_page: Point = page_offset

        x: int = page_offset.x
        y: int = page_offset.y
        offset: Point = Point(x, y)
        self.lower_left_offset = offset

        x: int = page_offset.x + BACKGROUND_SIZE.x
        y: int = page_offset.y
        offset: Point = Point(x, y)
        self.lower_right_offset: Point = offset

        x: int = page_offset.x
        y: int = page_offset.y + BACKGROUND_SIZE.y
        offset: Point = Point(x, y)
        self.upper_left_offset: Point = offset

        x: int = page_offset.x + BACKGROUND_SIZE.x
        y: int = page_offset.y + BACKGROUND_SIZE.y
        offset: Point = Point(x, y)
        self.upper_right_offset: Point = offset

        x: int = self.lower_left_offset.x + LABEL_MARGIN.x
        y: int = self.lower_left_offset.y + LABEL_MARGIN.y
        self.image_start: Point = Point(x, y)

        # title placement calculation
        x: int = self.upper_left_offset.x + (LABEL_SIZE.x // 2)
        y: int = self.upper_left_offset.y - LABEL_MARGIN.y
        self.title_start: Point = Point(x, y)
        return


class PrintLabelForm(forms.Form):
    """
    Form to request number of labels and starting number.
    """

    starting_number: int = forms.IntegerField()

    number_to_print: int = forms.IntegerField(
        initial=QR_LABELS_PER_PAGE,
        min_value=1,
        max_value=QR_LABELS_MAX,
    )


class PrintLabelView(PermissionRequiredMixin, View):
    """
    Manage the request for starting number and count of QR code to print.
    """

    permission_required = (
        'fpiweb.print_labels_box',
    )

    template_name = 'fpiweb/print_labels.html'
    form_class = PrintLabelForm
    success_url = reverse_lazy('fpiweb:index')

    @staticmethod
    def get_base_url(meta) -> str:
        """
        Determine the URL prefix to add to each QR code for a box.

        Modify this code as needed.

        :param meta:
        :return:
        """
        protocol = meta.get('SERVER_PROTOCOL', 'HTTP/1.1')
        protocol = protocol.split('/')[0].lower()

        host = meta.get('HTTP_HOST')
        # Real return value perhaps? = f"{protocol}://{host}/"
        return ""

    def get(self, request, *args, **kwargs):
        """
        Prepare to display request for starting box number and count.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # determine the highest numbered box in the database
        max_box_number: int = Box.objects.aggregate(Max(
            'box_number'))['box_number__max']
        logger.debug(f"max_box_number={max_box_number}")

        # add additional info to the default context
        get_context: dict = {
                'form': PrintLabelForm,
                'max_box_number': max_box_number,
                'labels_per_page': QR_LABELS_PER_PAGE,
                'labels_max': QR_LABELS_MAX,
        }

        # add navbar info
        get_context = add_navbar_vars(self.request.user, get_context)

        return render(
            request,
            self.template_name,
            get_context
        )

    def post(self, request, *args, **kwargs):
        """
        Validate the info returned from the user and generate the QR codes.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        base_url = self.get_base_url(request.META)

        form = PrintLabelForm(request.POST)
        if not form.is_valid():
            logger.debug("form invalid")
            return render(
                request,
                self.template_name,
                {'form': form},
            )
        logger.debug("form valid")

        # use an in memory buffer instead of a file so we don't have to
        # fuss with scratch files
        buffer = BytesIO()

        # generate the pages of QR codes in pdf format to the memory buffer
        QRCodePrinter(url_prefix=base_url).print(
            starting_number=form.cleaned_data.get('starting_number'),
            count=form.cleaned_data.get('number_to_print'),
            buffer=buffer,
        )

        # ensure that all of the pdf is in the memory buffer
        buffer.flush()

        # reset the pointer to the current position in the buffer back to
        # the beginning
        buffer.seek(0)

        # let Django pass the (memory) file in optimal chunks to the browser
        # as an attachment
        response = FileResponse(
            BufferedReader(buffer, buffer_size=DEFAULT_BUFFER_SIZE),
            as_attachment=True,
            filename="QR_labels.pdf"
        )
        return response


class QRCodePrinter(object):
    """
    Write the pdf of QR codes into the file or byte buffer provided.
    """

    def __init__(self, url_prefix: str):
        """
        Stash the url provided (if any) and establish some instance variables.

        :param url_prefix:
        """

        self.url_prefix = url_prefix
        self.box_start: int = 0
        self.label_count: int = 0
        self.buffer: Optional[BytesIO] = None

        self.pdf: Optional[Canvas] = None

        # # width and height are in points (1/72 inch)
        # width: int, height: int = letter
        # self.width: int = width
        # self.height: int = height

        # label locations on the page
        self.label_locations: List[LabelPosition] = list()
        self.compute_box_dimensions()

        # set this to the last position in the list to force a new page
        self.next_pos: int = len(self.label_locations)

        # use the page number to control first page handling
        self.page_number: int = 0

    def print(self, starting_number: int, count: int, buffer):
        """
        Starting point once view retrieved the requested info.

        :param starting_number: starting box number without the BOX prefix
        :param count: number of labels desired
        :param buffer: byte buffer to write pdf bytes into
        :return:
        """
        self.box_start: int = starting_number
        self.label_count: int = count
        self.buffer: BytesIO = buffer

        logger.debug(
            f'Parameters: pfx: {self.url_prefix}, '
            f'start: {self.box_start}, '
            f'count: {self.label_count}, '
        )

        self.generate_label_pdf()

        return

    def generate_label_pdf(self):
        """
        Generate the pdf file with the requested labels in it.

        :return:
        """

        self.initialize_pdf_file(self.buffer)
        self.fill_pdf_pages(self.box_start, self.label_count)
        self.finalize_pdf_file()
        return

    def initialize_pdf_file(self, buffer: BytesIO):
        """
        Prepare to scribble on a new pdf file.

        :param buffer:  May be a string with a filename or a BytesIO or other
            File-like object

        """
        self.pdf: Canvas = Canvas(buffer, pagesize=letter)
        return

    def compute_box_dimensions(self):
        """
        Compute the dimensions and bounding boxes for each label on the page.

        Called from __init__

        :return:
        """
        vertical_start: int = (BACKGROUND_SIZE.y * 3) + PAGE_OFFSET.y
        horizontal_stop: int = (BACKGROUND_SIZE.x * 3) + PAGE_OFFSET.x - 1
        for vertical_position in range(vertical_start, -1,
                                       -BACKGROUND_SIZE.y):
            for horizontal_position in range(PAGE_OFFSET.x,
                                             horizontal_stop,
                                             BACKGROUND_SIZE.x):
                new_label = \
                    LabelPosition(
                        Point(
                            horizontal_position,
                            vertical_position
                        )
                    )
                self.label_locations.append(new_label)
        return

    def fill_pdf_pages(self, starting_number: int, count: int):
        """
        Fill one or more pages with labels.

        draw lines around the boxes that will be filled with labels
        # self.draw_boxes_on_page()
        # self.pdf.setFillColorRGB(1, 0, 1)
        # self.pdf.rect(2*inch, 2*inch, 2*inch, 2*inch, fill=1)

        :return:
        """
        for label_file, label_name in self.get_next_qr_img(
            starting_number,
            count
        ):
            logger.debug(f'Got {label_file}')
            if self.next_pos >= len(self.label_locations) - 1:
                self.finish_page()
                self.next_pos = 0
            else:
                self.next_pos += 1
            self.draw_bounding_box(self.next_pos)
            self.place_label(label_file, label_name, self.next_pos)
        self.finish_page()
        return

    def place_label(self, file_name: str, label_name: str, pos: int):
        """
        Place the label in the appropriate location on the page.

        :param file_name:
        :param label_name:
        :param pos:
        :return:
        """
        box_info: LabelPosition = self.label_locations[pos]

        # place image on page
        im: Image = Image(file_name, LABEL_SIZE.x, LABEL_SIZE.y)
        im.drawOn(self.pdf, box_info.image_start.x, box_info.image_start.y)
        remove(file_name)

        # place title above image
        self.pdf.setFont('Helvetica-Bold', 12)
        self.pdf.drawCentredString(
            box_info.title_start.x + TITLE_ADJUSTMENT.x,
            box_info.title_start.y + TITLE_ADJUSTMENT.y,
            label_name
        )
        return

    def finish_page(self):
        """
        Finish off the previous page before starting a new one.
        """
        if self.page_number > 0:
            self.pdf.showPage()
        self.page_number += 1
        return

    def draw_bounding_box(self, label_pos: int):
        """
        Draw a bounding box around the specified label.

        :param label_pos: position in the labels locations list.
        :return:
        """
        box_info: LabelPosition = self.label_locations[label_pos]
        self.pdf.line(box_info.upper_left_offset.x,
                      box_info.upper_left_offset.y,
                      box_info.upper_right_offset.x,
                      box_info.upper_right_offset.y)
        self.pdf.line(box_info.upper_right_offset.x,
                      box_info.upper_right_offset.y,
                      box_info.lower_right_offset.x,
                      box_info.lower_right_offset.y)
        self.pdf.line(box_info.lower_right_offset.x,
                      box_info.lower_right_offset.y,
                      box_info.lower_left_offset.x,
                      box_info.lower_left_offset.y)
        self.pdf.line(box_info.lower_left_offset.x,
                      box_info.lower_left_offset.y,
                      box_info.upper_left_offset.x,
                      box_info.upper_left_offset.y)
        return

    def get_next_qr_img(self, start_number: int, count: int) -> (str, str):
        """
        Build the QR image for the next box label.

        :return: a QR code image file name and the prefixed box number
        """
        for url, label in self.get_next_box_url(start_number, count):
            label_file_name: str = f'{label}.png'
            qr = pyqrcode.create(url)
            qr.png(label_file_name, scale=5)
            yield label_file_name, label
        return

    def get_next_box_url(self, start_number: int, count: int) -> (str, str):
        """
        Build the URL for the next box.

        :return:
        """
        for label, box_number in self.get_next_box_number(
                start_number,
                count
        ):
            logger.debug(f'Got {label}, {box_number}')
            url: str = f"{self.url_prefix}{box_number:05}"
            yield url, label
        return

    @staticmethod
    def get_next_box_number(start, count) -> (str, int):
        """
        Search for the next box number to go on a label.

        :return:
        """
        next_box_number: int = start
        available_count: int = 0
        while available_count < count:
            box_label: str = f'BOX{next_box_number:05}'
            logger.debug(f'Attempting to get {box_label}')
            if Box.objects.filter(box_number=box_label).exists():
                next_box_number += 1
                continue
            available_count += 1
            logger.debug(f'{box_label} not found - using for label')
            yield box_label, next_box_number
            next_box_number += 1
        return

    def finalize_pdf_file(self):
        """
        All pages have been generated so flush all buffers and close.

        :return:
        """
        self.pdf.save()
        return

# EOF
