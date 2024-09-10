import datetime

from django import template

register = template.Library()


@register.filter
def custom_time_format(value):
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M")
    return value
