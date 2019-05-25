"""Standalone tool to print QR codes.

Usage:
    QRCodePrinter.py -p=<URL_prefix> -s <nnn> -c <nnn> -o <file>
    QRCodePrinter.py -h | --help
    QRCodePrinter.py --version

Options:
    -p <URL_prefix>, --prefix=<URL_prefix>   The URL prefix for the box number
    -s <nnn>, --start=<nnn>                  Starting box number to use
    -c <nnn>. --count=<nnn>                  Number of QR codes to print
    -o <file>, --output=<file>               Output file name
    -h --help             Show this help and quit.
    -v --version          Show the version of this program and quit.

"""

import logging
import logging.config
from logging import getLogger, debug, error
from pathlib import Path
from typing import Any, Union, Optional

from docopt import docopt
import yaml  # from PyYAML library

__author__ = 'Travis Risner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "05/22/2019"
# Copyright 2019 by Travis Risner - MIT License

log = None


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
        self.url_prefix: str = parm_dict['--prefix']
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
        debug(
            f'Parameters validated: pfx: {self.url_prefix}, '
            f'start: {self.box_start}, '
            f'count: {self.label_count}, '
            f'file: {self.output_file}'
        )
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
