from django import template

register = template.Library()


@register.filter(name="check_author")
def check_author(message, user):
    return message.author == user
