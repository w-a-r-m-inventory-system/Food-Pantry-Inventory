
from io import BytesIO
from logging import debug, getLogger
from dataclasses import dataclass, astuple, InitVar
from typing import List

import pyqrcode
import png
import qrcode.image.svg
import reportlab
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import Image

from fpiweb.models import Box

__author__ = 'Travis Risner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "09/09/2020"
# Copyright 2019 by Travis Risner - MIT License

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

logger = getLogger('fpiweb')


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
    LABEL_SIZE.y + (LABEL_MARGIN.y * 2))
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
        y = page_offset.y  + BACKGROUND_SIZE.y
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



class QRCodePrinter(object):
    """
    Write the pdf of QR codes into the byte buffer provided.
    """

    def __init__(self, url_prefix: str):

        self.url_prefix = url_prefix
        self.box_start: int = 0
        self.label_count: int = 0
        self.buffer: BytesIO

        self.pdf: Canvas

        # width and height are in points (1/72 inch)
        width, height = letter
        self.width: int = width
        self.height: int = height

        # label locations on the page
        self.label_locations: List[LabelPosition] = list()
        self.compute_box_dimensions()

        # set this to the last position in the list to force a new page
        self.next_pos: int = len(self.label_locations)

        # use the page number to control first page handling
        self.page_number: int = 0

    def print(self, starting_number: int, count: int, buffer: BytesIO):
        """
        Starting point once view retrieved the requested info.

        :param starting_number: starting box number without the BOX prefix
        :param count: number of labels desired
        :param buffer: byte buffer to write pdf bytes into
        :return:
        """
        self.box_start = starting_number
        self.label_count = count
        self.buffer = buffer

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
        self.pdf = Canvas(buffer, pagesize=letter)
        return

    def compute_box_dimensions(self):
        """
        Compute the dimensions and bounding boxes for each label on the page.

        Called from __init__

        :return:
        """
        vertical_start = (BACKGROUND_SIZE.y * 3) + PAGE_OFFSET.y
        horizontal_stop = (BACKGROUND_SIZE.x * 3) + PAGE_OFFSET.x - 1
        for vertical_position in range(vertical_start, -1,
                                       -BACKGROUND_SIZE.y):
            for horizontal_position in range(PAGE_OFFSET.x,
                                             horizontal_stop,
                                             BACKGROUND_SIZE.x):
                new_label = LabelPosition(Point(horizontal_position,
                                                vertical_position))
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
        box_info = self.label_locations[pos]

        # place image on page
        im = Image(file_name, LABEL_SIZE.x, LABEL_SIZE.y)
        im.drawOn(self.pdf, box_info.image_start.x, box_info.image_start.y)

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

    def get_next_qr_img(self, start_number: int, count: int) -> (str, str):
        """
        Build the QR image for the next box label.

        :return: a QR code image file name and the prefixed box number
        """
        for url, label in self.get_next_box_url(start_number, count):
            label_file_name = f'{label}.png'
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
            url = f"{self.url_prefix}{box_number:05}"
            yield url, label
        return

    @staticmethod
    def get_next_box_number(start, count) -> (str, int):
        """
        Search for the next box number to go on a label.

        :return:
        """
        next_box_number = start
        available_count = 0
        while available_count < count:
            box_label = f'BOX{next_box_number:05}'
            logger.debug(f'Attempting to get {box_label}')
            if Box.objects.filter(box_number=box_label).exists():
                next_box_number += 1
                continue
            available_count += 1
            logger.debug(f'{box_label} not found - using for label')
            yield box_label, next_box_number
            next_box_number += 1

    def finalize_pdf_file(self):
        self.pdf.save()
        return

# # # # ##
# The following code is needed by templatetags/qr_codes.py

# Combined path factory, fixes white space that may occur when zooming
factory = qrcode.image.svg.SvgPathImage

def get_qr_code_svg(data_string, include_xml_declaration=False):
    """
    Manages svg images

    :param include_xml_declaration:
    :return:
    """
    img = qrcode.make(data_string, image_factory=factory)

    with BytesIO() as bytes_out:
        img.save(bytes_out, kind='SVG')

        some_bytes = bytes_out.getvalue()
        svg = some_bytes.decode('utf-8')

        if not include_xml_declaration:
            svg = svg.split('?>\n')[-1]
        return svg

# EOF
