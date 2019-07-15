
from django.template import Library
from django.utils.safestring import mark_safe

from fpiweb.qr_code_utilities import get_qr_code_svg

register = Library()


@register.simple_tag
def qr_code(data_string):
    return mark_safe(get_qr_code_svg(data_string))

