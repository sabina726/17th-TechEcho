from django import template
from django.template.defaultfilters import date as date_filter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="teacher_icon")
def teacher_icon(user):
    if user.is_authenticated and user.is_teacher:
        return mark_safe(
            """
            <i class="fa-solid fa-glasses" style="color:#F28E13;"></i>
        """
        )
    return ""
