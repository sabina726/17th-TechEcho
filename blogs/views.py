from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BlogForm
from .models import Blog


def index(request):
    blogs = Blog.objects.filter(is_draft=False)  # Get only published blogs
    return render(request, "blogs/index.html", {"blogs": blogs})


@login_required
def user_drafts(request):
    # Get only drafts created by the current user
    drafts = Blog.objects.filter(author=request.user, is_draft=True)
    return render(request, "blogs/user_drafts.html", {"drafts": drafts})


@login_required
def new(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)  # Do not save to the database yet
            blog.author = (
                request.user
            )  # Assign the current logged-in user as the author

            action = request.POST.get("action")

            if action == "save_draft":
                blog.is_draft = True  # Save as a draft
                blog.save()
                return redirect("blogs:index")

            elif action == "preview":
                # Just render the preview page without saving
                return render(
                    request, "blogs/preview.html", {"blog": blog, "form": form}
                )

            elif action == "publish":
                blog.is_draft = False  # Publish the blog
                blog.save()
                return redirect("blogs:index")

        # If form is not valid, render the form again with errors
        return render(request, "blogs/new.html", {"form": form})

    else:
        form = BlogForm()
    return render(request, "blogs/new.html", {"form": form})


def show(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.views += 1
    blog.save()
    return render(request, "blogs/show.html", {"blog": blog})


@login_required
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


@login_required
def delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        blog.delete()
        return redirect("blogs:index")
    return render(request, "blogs/delete.html", {"blog": blog})
