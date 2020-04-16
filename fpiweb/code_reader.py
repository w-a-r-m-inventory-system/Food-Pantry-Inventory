
from base64 import b64decode
from binascii import Error as BinasciiError
from datetime import datetime
from logging import getLogger
from os import remove
from pathlib import Path
from random import seed, randint
from subprocess import run
from time import time

from django.conf import settings

from fpiweb.models import BoxNumber


logger = getLogger('fpiweb')

seed(time())

scan_data_prefix = 'data:image/png;base64,'


class CodeReaderError(RuntimeError):
    pass


def get_scan_file_path():
    scans_dir_path = Path(settings.SCANS_DIR)
    if not scans_dir_path.exists():
        raise OSError("{} doesn't exist".format(scans_dir_path))

    attempts = 100
    for i in range(attempts):
        filename = "{}_{:0>4}.png".format(
            datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
            randint(0, 9999),
        )
        path = scans_dir_path / filename
        if not path.exists():
            return path
    raise OSError(
        "Unable to generate path after {} attempts".format(attempts)
    )


def delete_file(image_file_path):
    logger.info(f"deleting {image_file_path}")
    remove(str(image_file_path))


def read(scan_data):

    if not scan_data.startswith(scan_data_prefix):
        raise CodeReaderError('Invalid scan data')

    logger.info("scan_data is {:,} characters in length".format(
        len(scan_data)))

    try:
        scan_data_bytes = b64decode(
            scan_data[len(scan_data_prefix):]
        )
    except BinasciiError as e:
        raise CodeReaderError(str(e))

    try:
        image_file_path = get_scan_file_path()
    except OSError as e:
        raise CodeReaderError(str(e))

    logger.info(f"writing file to {image_file_path}")
    with image_file_path.open('wb') as image_file:
        image_file.write(scan_data_bytes)

    program_name = 'zbarimg'
    try:
        completed_process = run(
            [program_name, str(image_file_path)],
            capture_output=True,
            timeout=5,  # 5 seconds to run
        )
    except FileNotFoundError as error:
        error_message = str(error)
        logger.error(error_message)
        if program_name in error_message:
            logger.error(
                error_message +
                ".  Is the zbar-tools package installed.  "
                "Use sudo apt-get install zbar-tools to install it.")
        raise CodeReaderError(error_message)
    except RuntimeError as error:
        error_message = "{}.  error is a {}".format(
            str(error),
            type(error),
        )
        logger.error(error_message)
        raise CodeReaderError(error_message)

    if completed_process.returncode != 0:
        error_message = completed_process.stderr.decode()
        logger.error(error_message)
        delete_file(image_file_path)
        raise CodeReaderError(error_message)

    delete_file(image_file_path)
    qr_data = completed_process.stdout.decode()
    return qr_data


def read_box_number(scan_data):

    qr_data = read(scan_data)

    match = BoxNumber.box_number_search_regex.search(qr_data)
    if not match:
        error_message = f"box number not found in {qr_data}"
        logger.error(error_message)
        raise CodeReaderError(error_message)

    box_number = match.group().upper()
    logger.info(f"scanned box_number is {box_number}")
    return box_number
