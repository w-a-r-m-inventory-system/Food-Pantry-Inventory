"""Standalone tool to print QR codes.

Usage:
    QRCodePrinter.py -p=<URL_prefix> -s <nnn> -c <nnn> -o <file>
    QRCodePrinter.py -h | --help
    QRCodePrinter.py --version

Options:

    -p <URL_prefix>, --prefix=<URL_prefix>   The URL prefix for the box number
    -s <nnn>, --start=<nnn>                  Starting box number to use
    -c <nnn>, --count=<nnn>                  Number of QR codes to print
    -o <file>, --output=<file>               Output file name
    -h, --help                                Show this help and quit.
    -v, --version                             Show the version of this program and quit.

"""

import logging
import logging.config
from dataclasses import dataclass, astuple, InitVar
from logging import getLogger, debug, error
from pathlib import Path
from typing import Any, Union, Optional, NamedTuple, List

from docopt import docopt
import pyqrcode
import png
import reportlab
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import Image
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select
import yaml  # from PyYAML library

from FPIDjango.private import settings_private

__author__ = 'Travis Risner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "05/22/2019"
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

log = None


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


class QRCodePrinterClass:
    """
    QRCodePrinterClass - Print QR Codes
    """

    def __init__(self, workdir: Path):
        self.working_dir: Path = None
        self.url_prefix: str = ''
        self.box_start: int = 0
        self.label_count: int = 0
        self.output_file: str = ''
        self.full_path: Path = None
        self.pdf: Canvas = None

        # width and height are in points (1/72 inch)
        self.width: int = None
        self.height: int = None

        # database connection information
        self.con = None
        self.meta: MetaData = None
        self.box: Table = None

        # label locations on the page
        self.label_locations: List[LabelPosition] = list()
        self.compute_box_dimensions()

        # set this to the last position in the list to force a new page
        self.next_pos: int = len(self.label_locations)

        # use the page number to control first page handling
        self.page_number: int = 0

        if not workdir is None and workdir.is_dir():
            self.working_dir = workdir
        return

    def run_QRPrt(self, parameters: dict):
        """
        Top method for running Run the QR code printer..

        :param parameters: dictionary of command line arguments
        :return:
        """
        parm_dict = parameters
        self.url_prefix: str = parm_dict['--prefix'].strip('\'"')
        self.box_start: int = int(parm_dict['--start'])
        self.label_count: int = int(parm_dict['--count'])
        self.output_file: str = parm_dict['--output']
        if (not isinstance(self.box_start, int)) or \
                self.box_start <= 0:
            raise ValueError('Box start must be a positive integer')
        if (not isinstance(self.label_count, int)) or \
                self.label_count <= 0:
            raise ValueError('Label count must be a positive integer')
        full_path = self.working_dir / self.output_file
        if full_path.exists():
            raise ValueError('File already exists')
        else:
            self.full_path = full_path
        debug(
            f'Parameters validated: pfx: {self.url_prefix}, '
            f'start: {self.box_start}, '
            f'count: {self.label_count}, '
            f'file: {self.output_file}'
        )

        self.connect_to_generate_labels()
        return

    def connect_to_generate_labels(self):
        """
        Connect to the database and generate labels.
        :return:
        """
        # establish access to the database
        self.con, self.meta = self.connect(
            user=settings_private.DB_USER,
            password=settings_private.DB_PSWD,
            db=settings_private.DB_NAME,
            host=settings_private.DB_HOST,
            port=settings_private.DB_PORT
        )

        # establish access to the box table
        self.box = Table(
            'fpiweb_box',
            self.meta,
            autoload=True,
            autoload_with=self.con)

        self.generate_label_pdf()
        # self.con.close()
        return

    def connect(self, user, password, db, host='localhost', port=5432):
        """
        Establish a connection to the desired PostgreSQL database.

        :param user:
        :param password:
        :param db:
        :param host:
        :param port:
        :return:
        """

        # We connect with the help of the PostgreSQL URL
        # postgresql://federer:grandestslam@localhost:5432/tennis
        url = f'postgresql://{user}:{password}@{host}:{port}/{db}'

        # The return value of create_engine() is our connection object
        con = create_engine(url, client_encoding='utf8')
        # We then bind the connection to MetaData()
        meta = MetaData(bind=con)
        return con, meta

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
        self.pdf = Canvas(str(self.full_path), pagesize=letter)
        self.width, self.height = letter

        return

    def compute_box_dimensions(self):
        """
        Compute the dimensions and bounding boxes for each label on the page.
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
                self. finish_page()
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

    def get_next_qr_img(self) -> (str, str):
        """
        Build the QR image for the next box label.

        :return: a QR code image ready to print
        """
        for url, label in self.get_next_box_url():
            label_file_name = f'{label}.png'
            qr = pyqrcode.create(url)
            qr.png(label_file_name, scale=5)
            yield label_file_name, label
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
        Search for the next box number to go on a label.

        :return:
        """
        next_box_number = self.box_start
        available_count = 0
        while available_count < self.label_count:
            box_label = f'BOX{next_box_number:05}'
            debug(f'Attempting to get {box_label}')
            sel_box_stm = select([self.box]).where(
                self.box.c.box_number == box_label)
            # box_found = exists(sel_box_stm)
            # exist_stm = exists().where(self.box.c.box_number == box_label)
            result = self.con.execute(sel_box_stm)
            debug(f'Search result: {result.rowcount}')
            box = result.fetchone()
            if not box:
                # found a hole in the numbers
                available_count += 1
                debug(f'{box_label} not found - using for label')
                yield (box_label, next_box_number)
            else:
                result.close()
            next_box_number += 1
        return

    def finalize_pdf_file(self):
        """
        All pages have been generated so flush all buffers and close.

        :return:
        """
        self.pdf.save()
        return


class Main:
    """
    Main class to start things rolling.
    """

    def __init__(self):
        """
        Get things started.
        """
        self.QRCodePtr: QRCodePrinterClass = None
        self.working_dir: Path = None
        return

    def run_QRCodePtr(self, arguments: dict):
        """
        Prepare to run Run the QR code printer..

        :return:
        """
        self.QRCodePtr = QRCodePrinterClass(workdir=self.working_dir)
        debug('Starting up QRCodePtr')
        self.QRCodePtr.run_QRPrt(arguments)
        return

    def start_logging(self, work_dir: Path, debug_name: str):
        """
        Establish the logging for all the other scripts.

        :param work_dir:
        :param debug_name:
        :return: (nothing)
        """

        # Set flag that no logging has been established
        logging_started = False

        # find our working directory and possible logging input file
        _workdir = work_dir
        _logfilename = debug_name

        # obtain the full path to the log information
        _debugConfig = _workdir / _logfilename

        # verify that the file exists before trying to open it
        if Path.exists(_debugConfig):
            try:
                #  get the logging params from yaml file and instantiate a log
                with open(_logfilename, 'r') as _logdictfd:
                    _logdict = yaml.load(_logdictfd, Loader=yaml.SafeLoader)
                logging.config.dictConfig(_logdict)
                logging_started = True
            except Exception as xcp:
                print(f'The file {_debugConfig} exists, but does not contain '
                      f'appropriate logging directives.')
                raise ValueError('Invalid logging directives.')
        else:
            print(f'Logging directives file {_debugConfig} either not '
                  f'specified or not found')

        if not logging_started:
            # set up minimal logging
            _logfilename = 'debuginfo.txt'
            _debugConfig = _workdir / _logfilename
            logging.basicConfig(filename='debuginfo.txt', level=logging.INFO,
                                filemode='w')
            print(f'Minimal logging established to {_debugConfig}')

        # start logging
        global log
        log = logging.getLogger(__name__)
        logging.info(f'Logging started: working directory is {_workdir}')

        # sset confirmed working directory to pass on to target class
        self.working_dir = _workdir
        return


if __name__ == "__main__":
    arguments = docopt(__doc__, version='QRCodePrinter 1.0')
    workdir = Path.cwd()
    debug_file_name = 'debug_info.yaml'
    main = Main()
    main.start_logging(workdir, debug_file_name)
    debug('Parameters as interpreted by docopt')
    for arg in arguments:
        debug(f'arg key: {arg}, value: {arguments[arg]}')
    main.run_QRCodePtr(arguments)

# EOF
