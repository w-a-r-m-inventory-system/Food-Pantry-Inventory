
from django.template import Library
from django.utils.safestring import mark_safe

from fpiweb.qr_code_utilities import get_qr_code_svg

register = Library()


@register.simple_tag
def qr_code(data_string):
    """
    Interface to allow a URL to be converted into a QR code.

    :param data_string: URL to be conveted
    :return: image of QR code
    """
    return mark_safe(get_qr_code_svg(data_string))

