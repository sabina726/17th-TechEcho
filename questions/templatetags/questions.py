from django import template

register = template.Library()


@register.filter(name="questions_votes")
def questions_votes(vote, condition):
    return "500" if vote == condition else "300"


@register.filter(name="questions_labels")
def questions_labels(question):
    return question.labels.all()
