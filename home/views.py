from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render

from blogs.models import Blog
from questions.models import Question
from teachers.models import Teacher


def index(request):
    return render(request, "home/index.html")


def privacy(request):
    return render(request, "home/privacy.html")


def terms(request):
    return render(request, "home/terms.html")


def search(request):
    query = request.GET.get("q", "")
    search_terms = []
    questions = Question.objects.none()
    blogs = Blog.objects.none()
    teachers = Teacher.objects.none()

    if query:
        search_terms = query.split()

        q_objects = Q()
        for term in search_terms:
            q_objects |= (
                Q(title__icontains=term)
                | Q(details__icontains=term)
                | Q(labels__name__icontains=term)
            )

        questions = Question.objects.filter(q_objects).distinct()

        blog_q_objects = Q()
        for term in search_terms:
            blog_q_objects |= (
                Q(title__icontains=term)
                | Q(content__icontains=term)
                | Q(labels__name__icontains=term)
            )

        blogs = Blog.objects.filter(blog_q_objects).distinct()

        teacher_q_objects = Q()
        for term in search_terms:
            teacher_q_objects |= (
                Q(labels__name__icontains=term)
                | Q(user__username__icontains=term)
                | Q(user__nickname__icontains=term)
            )

        teachers = Teacher.objects.filter(teacher_q_objects).distinct()

    else:
        messages.info(request, "請輸入搜尋內容")

    return render(
        request,
        "home/search.html",
        {
            "questions": questions,
            "teachers": teachers,
            "blogs": blogs,
            "query": query,
        },
    )
