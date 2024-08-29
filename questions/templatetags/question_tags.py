from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="question_tags")
def question_tags(question):
    return question.tags.all()
