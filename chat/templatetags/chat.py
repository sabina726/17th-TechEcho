from django import template

register = template.Library()


@register.filter(name="check_author")
def check_author(message, user):
    return "start" if message.author != user else "end"
