from django import template
from django.conf import settings
register = template.Library()


@register.simple_tag
def web_name():
    return settings.WEB_NAME


@register.simple_tag
def base_dir():
    return settings.BASE_DIR


@register.filter(name='embed_url')
def embed_url(url):
    return url.replace("watch?v=", "embed/")

embed_url.is_safe = True


@register.filter(name='if_in_list')
def if_in_list(value, string_list):
    my_list = string_list.split(',')
    if str(value) in my_list:
      return True
    return False