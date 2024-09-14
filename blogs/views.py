from django.shortcuts import get_object_or_404, redirect, render
from .forms import BlogForm  # Assume you have a BlogForm instead of ArticleForm
from .models import Blog  # Assume you have a Blog model instead of Article

def index(request):
    # Fetch all blog entries ordered by creation date
    blogs = Blog.objects.all().order_by("-created_at")
    return render(request, "blogs/index.html", {'blogs': blogs})

def show(request, pk):
    # Get a specific blog by its primary key (pk)
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, "blogs/show.html", {'blog': blog})

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
    # Get a specific blog to edit by its primary key (pk)
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect("blogs:show", pk=blog.pk)
    else:
        form = BlogForm(instance=blog)
    return render(request, "blogs/edit.html", {"form": form})

def delete(request, pk):
    # Get a specific blog to delete by its primary key (pk)
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        blog.delete()
        return redirect("blogs:index")
    return render(request, "blogs/delete.html", {'blog': blog})