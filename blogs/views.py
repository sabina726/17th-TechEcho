from django.shortcuts import get_object_or_404, redirect, render

from .forms import BlogForm
from .models import Blog


def index(request):
    blogs = Blog.objects.all().order_by("-created_at")
    return render(request, "blogs/index.html", {"blogs": blogs})


def show(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, "blogs/show.html", {"blog": blog})


def new(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("blogs:index")
    else:
        form = BlogForm()
    return render(request, "blogs/new.html", {"form": form})


def edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect("blogs:show", pk=blog.pk)
    else:
        form = BlogForm(instance=blog)
    return render(request, "blogs/edit.html", {"form": form, "blog": blog})


def delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        blog.delete()
        return redirect("blogs:index")
    return render(request, "blogs/delete.html", {"blog": blog})
