from django import template
from django.conf import settings
register = template.Library()


@register.simple_tag
def web_name():
    return settings.WEB_NAME


@register.simple_tag
def base_dir():
    return settings.BASE_DIR
