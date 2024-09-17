import uuid

import bleach
import markdown
from bleach.sanitizer import ALLOWED_TAGS
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BlogForm
from .models import Blog


@login_required  # Ensure only authenticated users can upload images
def image_upload(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]

        # Validate file size (e.g., max 2MB)
        if image.size > 2 * 1024 * 1024:
            return JsonResponse({"error": "File too large (max 2MB)."}, status=400)

        # Validate file type
        if not image.content_type.startswith("image/"):
            return JsonResponse({"error": "Invalid file type."}, status=400)

        # Generate a unique filename
        extension = image.name.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{extension}"

        # Save the image to MEDIA_ROOT/uploads/
        save_path = default_storage.save(
            "uploads/" + unique_filename, ContentFile(image.read())
        )
        image_url = settings.MEDIA_URL + save_path

        return JsonResponse({"url": image_url})

    return JsonResponse({"error": "Invalid request"}, status=400)


def index(request):
    blogs = Blog.objects.filter(is_draft=False).order_by("-created_at")
    return render(request, "blogs/index.html", {"blogs": blogs})


@login_required
def user_drafts(request):
    drafts = Blog.objects.filter(author=request.user, is_draft=True).order_by(
        "-created_at"
    )
    return render(request, "blogs/user_drafts.html", {"drafts": drafts})


@login_required
def new(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user

            action = request.POST.get("action")

            if action == "save_draft":
                blog.is_draft = True
                blog.save()
                return redirect("blogs:index")

            elif action == "preview":
                # Convert and sanitize content for preview
                raw_html = markdown.markdown(blog.content)

                # Corrected line
                allowed_tags = ALLOWED_TAGS.union(
                    {"img", "p", "div", "span", "h1", "h2", "h3", "h4", "h5", "h6"}
                )
                allowed_attributes = {"img": ["src", "alt", "title"]}
                content_html = bleach.clean(
                    raw_html, tags=allowed_tags, attributes=allowed_attributes
                )

                return render(
                    request,
                    "blogs/preview.html",
                    {"blog": blog, "form": form, "content_html": content_html},
                )

            elif action == "publish":
                blog.is_draft = False
                blog.save()
                return redirect("blogs:index")

        return render(request, "blogs/new.html", {"form": form})

    else:
        form = BlogForm()
    return render(request, "blogs/new.html", {"form": form})


def show(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    # Convert Markdown to HTML with useful extensions
    content_html = markdown.markdown(
        blog.content,
        extensions=[
            "markdown.extensions.extra",  # Provides extra features like footnotes, tables, etc.
            "markdown.extensions.codehilite",  # Syntax highlighting for code blocks
            "markdown.extensions.toc",  # Table of Contents support
            "markdown.extensions.sane_lists",  # Improved list handling
        ],
    )

    # Increment view count safely
    Blog.objects.filter(pk=pk).update(views=blog.views + 1)

    return render(
        request, "blogs/show.html", {"blog": blog, "content_html": content_html}
    )


@login_required
def edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    # Authorization check
    if blog.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this blog post.")

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

    # Authorization check
    if blog.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this blog post.")

    if request.method == "POST":
        blog.delete()
        return redirect("blogs:index")
    return render(request, "blogs/delete.html", {"blog": blog})
