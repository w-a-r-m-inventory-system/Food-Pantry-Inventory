"""
qr_code_utilities.py - support code for scanning QR codes.
"""
from io import BytesIO
from logging import getLogger

import qrcode
import qrcode.image.svg

__author__ = 'Travis Risner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "09/09/2020"


logger = getLogger('fpiweb')

# Combined path factory, fixes white space that may occur when zooming
factory = qrcode.image.svg.SvgPathImage


# # # # ##
# The following code is needed by templatetags/qr_codes.py

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
