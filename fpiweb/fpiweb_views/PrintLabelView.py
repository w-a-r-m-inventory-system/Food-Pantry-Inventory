"""
PrintlabelView.py - manage the view to print QR codes on labels.
"""
import logging
import logging.config
from dataclasses import dataclass, astuple, InitVar
from logging import getLogger, debug, error
from pathlib import Path
from typing import Any, Union, Optional, NamedTuple, List
from io import BytesIO

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Max
from django import forms
from django.http import FileResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
import pyqrcode
import png
import reportlab
from django.views.generic import FormView
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import Image
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select
import yaml  # from PyYAML library

from fpiweb.constants import UserInfo
from fpiweb.models import Box
# from fpiweb.qr_code_utilities import QRCodePrinter
from FPIDjango.private import settings_private

__author__ = 'Travis Risner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "07/22/2020"
# Copyright 2020 by Travis Risner - MIT License
from fpiweb.support.PermissionsManagement import ManageUserPermissions

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
        self.offset_on_page = page_offset

        x: int = page_offset.x
        y: int = page_offset.y
        offset: Point = Point(x, y)
        self.lower_left_offset = offset

        x = page_offset.x + BACKGROUND_SIZE.x
        y = page_offset.y
        offset: Point = Point(x, y)
        self.lower_right_offset = offset

        x = page_offset.x
        y = page_offset.y + BACKGROUND_SIZE.y
        offset: Point = Point(x, y)
        self.upper_left_offset = offset

        x = page_offset.x + BACKGROUND_SIZE.x
        y = page_offset.y + BACKGROUND_SIZE.y
        offset: Point = Point(x, y)
        self.upper_right_offset = offset

        x = self.lower_left_offset.x + LABEL_MARGIN.x
        y = self.lower_left_offset.y + LABEL_MARGIN.y
        self.image_start: Point = Point(x, y)

        # title placement calculation
        x = self.upper_left_offset.x + (LABEL_SIZE.x // 2)
        y = self.upper_left_offset.y - LABEL_MARGIN.y
        self.title_start: Point = Point(x, y)
        return


class PrintLabelForm(forms.Form):

    starting_number = forms.IntegerField()

    number_to_print = forms.IntegerField(
        initial=4,
    )


class PrintLabelView(PermissionRequiredMixin, View):
    permission_required = ('fpiweb.print_labels_box',)

    template_name = 'fpiweb/print_labels.html'
    form_class = PrintLabelForm
    success_url = reverse_lazy('fpiweb:index')

    def __init__(self):
        _ = super().__init__()
        self.url_prefix: str = 'BOX'
        self.box_start: int = 0
        self.label_count: int = 12
        self.working_dir: Path = Path.cwd()
        self.canvas_file: Path = self.working_dir / 'QR Sheets.pdf'
        self.pdf: Optional[Canvas] = None

        # width and height are in points (1/72 inch)
        self.width: Optional[int] = None
        self.height: Optional[int] = None

        # label locations on the page
        self.label_locations: List[LabelPosition] = list()
        self.compute_box_dimensions()

        # set this to the last position in the list to force a new page
        self.next_pos: int = len(self.label_locations)

        # provide support for user in page heading
        self.pm = ManageUserPermissions()

        # use the page number to control first page handling
        self.page_number: int = 0
        return

    @staticmethod
    def get_base_url(meta):
        """
        Get the base URL to use as a prefix to the box number.

        Change this code if we ever need a prefix to the box number.

        :param meta:
        :return:
        """
        # protocol = meta.get('SERVER_PROTOCOL', 'HTTP/1.1')
        # protocol = protocol.split('/')[0].lower()
        #
        # host = meta.get('HTTP_HOST')
        # return f"{protocol}://{host}/"
        return ""

    def get(self, request, *args, **kwargs):
        """
        Prepare the print label view.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # get permission level and other info about current user
        this_user = request.user
        this_user_info: UserInfo = self.pm.get_user_info(user_id=this_user.id)

        # Preset the box number to the maximum box number so far
        max_box_number = Box.objects.aggregate(Max('box_number'))
        max_box_name = max_box_number['box_number__max']
        if max_box_name:
            next_number = int(max_box_name[3:]) + 1
        else:
            next_number = 1
        form = PrintLabelForm()
        form.initial['starting_number'] = next_number
        form.initial['number_to_print'] = self.label_count
        context = dict()
        context['this_user_info'] = this_user_info
        context['form'] = form
        context['labels_per_page'] = self.label_count

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        base_url = self.get_base_url(request.META)

        form = PrintLabelForm(request.POST)
        if not form.is_valid():
            print("form invalid")
            return render(request, self.template_name, {'form': form}, )
        starting_number = form.cleaned_data['starting_number']
        labels_to_print = form.cleaned_data['number_to_print']
        debug(f'Printing {labels_to_print} starting at {starting_number}')

        self.run_QRPrt(url_prefix='', starting_number=starting_number,
                       count=labels_to_print)

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        # self.pdf.seek(0)
        return FileResponse(
            open(self.canvas_file, mode='rb'),
            as_attachment=True,
            filename='QR Code Sheets.pdf'
        )

    def run_QRPrt(self,
                  url_prefix: str = '',
                  starting_number: int = 1,
                  count: int = 0,
                  buffer: Optional[BytesIO] = None
                  ):
        """
        Generate the requested labels as a PDF.

        :param starting_number: starting box number
        :param count: number of labels to print
        :param buffer: byte buffer to hold pdf
        :return: (PDF formatted label file is in the buffer
        """
        self.url_prefix: str = url_prefix
        self.box_start: int = starting_number
        self.label_count: int = count
        self.buffer: BytesIO = buffer
        # self.output_file: BytesIO = buffer

        debug(f'Parameters validated: pfx: {self.url_prefix}, '
              f'start: {self.box_start}, '
              f'count: {self.label_count}'
        )
        self.generate_label_pdf()
        return

    def generate_label_pdf(self):
        """
        Generate the pdf file with the requested labels in it.
        :return:
        """
        self.initialize_pdf_file()
        self.fill_pdf_pages()
        self.finalize_pdf_file()
        return

    def initialize_pdf_file(self):
        """
        Setup the pdf to receive labels.

        :return:
        """
        self.pdf = Canvas(str(self.canvas_file), pagesize=letter)
        self.width, self.height = letter

        return

    def compute_box_dimensions(self):
        """
        Compute the dimensions and bounding boxes for each label on the page.
        :return:
        """
        vertical_start = (BACKGROUND_SIZE.y * 3) + PAGE_OFFSET.y
        horizontal_stop = (BACKGROUND_SIZE.x * 3) + PAGE_OFFSET.x - 1
        for vertical_position in range(vertical_start, -1, -BACKGROUND_SIZE.y):
            for horizontal_position in range(PAGE_OFFSET.x, horizontal_stop,
                                             BACKGROUND_SIZE.x):
                new_label = LabelPosition(
                    Point(horizontal_position, vertical_position))
                self.label_locations.append(new_label)
        return

    def fill_pdf_pages(self):
        """
        Fill one or more pages with labels.

        :return:
        """
        # # draw lines around the boxes that will be filled with labels
        # self.draw_boxes_on_page()
        # # self.pdf.setFillColorRGB(1, 0, 1)
        # # self.pdf.rect(2*inch, 2*inch, 2*inch, 2*inch, fill=1)
        for label_file, label_name in self.get_next_qr_img():
            debug(f'Got {label_file}')
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
        box_info = self.label_locations[pos]

        # place image on page
        im = Image(file_name, LABEL_SIZE.x, LABEL_SIZE.y)
        im.drawOn(self.pdf, box_info.image_start.x, box_info.image_start.y)

        # place title above image
        self.pdf.setFont('Helvetica-Bold', 12)
        self.pdf.drawCentredString(box_info.title_start.x + TITLE_ADJUSTMENT.x,
                                   box_info.title_start.y + TITLE_ADJUSTMENT.y,
            label_name)

        # now that we are done with the QR code image, delete the file.
        Path.unlink(file_name, missing_ok=True)
        return

    def finish_page(self):
        """
        Finish off the prefious page before starting a new one
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
        box_info = self.label_locations[label_pos]
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

    def get_next_qr_img(self) -> (str, str):
        """
        Build the QR image for the next box label.

        :return: a QR code image ready to print
        """
        for url, label in self.get_next_box_url():
            label_file = self.working_dir / f'{label}.png'
            qr = pyqrcode.create(url)
            qr.png(label_file, scale=5)
            yield label_file, label
        return

    def get_next_box_url(self) -> (str, str):
        """
        Build the URL for the next box.
        :return:
        """
        for label, box_number in self.get_next_box_number():
            debug(f'Got {label}, {box_number}')
            url = f"{self.url_prefix}{box_number:05}"
            yield url, label
        return

    def get_next_box_number(self) -> (str, int):
        """
        Generator to identify the next box number to go on a label.

        :return:
        """
        next_box_number = self.box_start
        available_count = 0
        while available_count < self.label_count:
            box_label = f'BOX{next_box_number:05}'
            debug(f'Attempting to get {box_label}')
            if not Box.objects.filter(box_number=box_label).exists():
                # found a hole in the numbers
                available_count += 1
                debug(f'{box_label} not found - using for label')
                yield (box_label, next_box_number)
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
