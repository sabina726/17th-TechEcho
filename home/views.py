import json

from django.db.models import Q
from django.shortcuts import render

from questions.models import Question


def index(request):
    if request.user.is_authenticated:
        context = {"user": request.user, "is_authenticated": True}
    else:
        context = {"is_authenticated": False}
    return render(request, "home/index.html", context)


def search_view(request):
    query = request.GET.get("q", "")
    allowed_terms = {"Python", "Ruby", "JavaScript"}
    search_terms = []

    if query:
        try:
            tags = json.loads(query)
            search_terms = [
                tag.get("value", query)
                for tag in (tags if isinstance(tags, list) else [tags])
                if isinstance(tag, dict) and tag.get("value") in allowed_terms
            ]
        except json.JSONDecodeError:
            if query in allowed_terms:
                search_terms.append(query)

        # Construct the search query
        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(title__icontains=term) | Q(details__icontains=term)

        # Filter questions based on search terms
        questions = Question.objects.filter(q_objects).distinct()

    # Render the full page for normal requests

    return render(
        request,
        "home/search_result.html",
        {
            "questions": questions,
            "query": ", ".join(search_terms),
        },
    )
