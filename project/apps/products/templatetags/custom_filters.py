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
