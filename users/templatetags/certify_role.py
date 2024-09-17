from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="teacher_icon")
def teacher_icon(user):
    if user and user.is_teacher:
        return mark_safe("<i class='fa-solid fa-glasses'></i>")

    return ""
