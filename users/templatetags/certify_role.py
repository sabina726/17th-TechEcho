from django import template
from django.template.defaultfilters import date as date_filter

register = template.Library()

@register.filter(name="standard_date")
def standard_date(value):
    return date_filter(value, "Y/m/d H:i")
