import json

from django.db.models import Q
from django.shortcuts import render

from questions.models import Question


def home_index(request):
    return render(request, "home/index.html")


def search_form_index(request):
    return render(request, "search/search_form.html")


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

        if search_terms:
            q_objects = Q()
            for term in search_terms:
                q_objects |= Q(title__icontains=term) | Q(details__icontains=term)

            results = Question.objects.filter(q_objects).distinct()
        else:
            results = []

    return render(
        request,
        "search/search_form.html",
        {
            "results": results,
            "query": ", ".join(search_terms),
            "search_terms": json.dumps(search_terms),
        },
    )
