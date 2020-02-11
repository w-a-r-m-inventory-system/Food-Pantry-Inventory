from django import template


register = template.Library()


@register.simple_tag
def initial_or_cleaned(form, field_name):
    value = form.initial.get(field_name)
    if value:
        return str(value)
    value = form.cleaned_data.get(field_name)
    if value:
        return str(value)
    return ""