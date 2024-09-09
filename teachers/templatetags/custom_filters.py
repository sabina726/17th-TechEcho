from django import template
import datetime

register = template.Library()


@register.filter
def custom_time_format(value):
    if isinstance(value, datetime.time):
        return (
            "12:00 AM"
            if value.hour == 0 and value.minute == 0
            else (
                "12:00 PM"
                if value.hour == 12 and value.minute == 0
                else value.strftime("%I:%M %p")
            )
        )
    return value
