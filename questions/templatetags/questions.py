from django import template

register = template.Library()

@register.filter(name="questions_votes")
def questions_votes(vote, condition):
    return "500" if vote == condition else "300"