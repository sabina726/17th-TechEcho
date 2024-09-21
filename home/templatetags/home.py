from django import template
from django.template.defaultfilters import date as date_filter
from django.utils.timezone import localtime

register = template.Library()


@register.filter(name="standard_date")
def standard_date(value):
    value = localtime(value)
    return date_filter(value, "Y/m/d H:i")
