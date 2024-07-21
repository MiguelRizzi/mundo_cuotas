from django import template
from products.utils import validate_img_extension, validate_video_extension

register = template.Library()

@register.filter(name="determine_file_type")
def determine_file_type(file):
    if validate_img_extension(file):
        return 'image'
    elif validate_video_extension(file):
        return 'video'
    else:
        return 'other'



@register.filter
def format_number_with_commas(value, decimal_places=None):
    try:
        value = float(value)
        if decimal_places is not None:
            pre_formated_Value ='{:,.{}f}'.format(value, decimal_places).replace(",", ".")
            formated_value = pre_formated_Value[:-3] + "," + pre_formated_Value[-2:]
            return formated_value
        else:
            return '{:,.2f}'.format(value).replace(",", ".")
    except (TypeError, ValueError):
        return value