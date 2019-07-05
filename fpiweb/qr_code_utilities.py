
from io import BytesIO

import qrcode.image.svg

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
