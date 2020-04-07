
from io import BytesIO
from logging import getLogger

from pyqrcode import create as create_qrcode

import qrcode.image.svg

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter

from fpiweb.models import Box


logger = getLogger('fpiweb')

# Combined path factory, fixes white space that may occur when zooming
factory = qrcode.image.svg.SvgPathImage


def get_qr_code_svg(data_string, include_xml_declaration=False):
    img = qrcode.make(data_string, image_factory=factory)

    with BytesIO() as bytes_out:
        img.save(bytes_out, kind='SVG')

        some_bytes = bytes_out.getvalue()
        svg = some_bytes.decode('utf-8')

        if not include_xml_declaration:
            svg = svg.split('?>\n')[-1]
        return svg


class QRCodePrinter(object):

    def __init__(self, url_prefix):

        self.url_prefix = url_prefix

        self.pdf: Canvas

        width, height = letter
        self.width: int = width
        self.height: int = height
        self.next_pos = 0

    def initialize_pdf_file(self, buffer):
        """
        Prepare to scribble on a new pdf file.

        :param buffer:  May be a string with a filename or a BytesIO or other
            File-like object

        """
        self.pdf: Canvas(buffer, pagesize=letter)

    @staticmethod
    def get_box_numbers(start, count) -> (str, int):
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

    def get_next_box_url(self, starting_number, count) -> (str, str):
        """
        Build the URL for the next box.
        :return:
        """
        for label, box_number in self.get_box_numbers(
            starting_number,
            count
        ):
            logger.debug(f'Got {label}, {box_number}')
            url = f"{self.url_prefix}{box_number:05}"
            yield url, label

    def get_next_qr_img(self, starting_number, count) -> (str, str):
        """
        Build the QR image for the next box label.

        :return: a QR code image ready to print
        """
        for url, label in self.get_next_box_url(starting_number, count):
            label_file_name = f'{label}.png'
            qr = create_qrcode(url)
            qr.png(label_file_name, scale=5)
            yield label_file_name, label

    def fill_pdf_pages(self, starting_number, count):
        # # draw lines around the boxes that will be filled with labels
        # self.draw_boxes_on_page()
        # # self.pdf.setFillColorRGB(1, 0, 1)
        # # self.pdf.rect(2*inch, 2*inch, 2*inch, 2*inch, fill=1)
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

    @staticmethod
    def finalize_pdf_file():
        pass

    def print(self, starting_number, count, buffer):
        self.initialize_pdf_file(buffer)
        self.fill_pdf_pages(starting_number, count)
        self.finalize_pdf_file()

