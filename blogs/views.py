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


@login_required
def image_upload(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]

        if image.size > 2 * 1024 * 1024:
            return JsonResponse({"error": "File too large (max 2MB)."}, status=400)

        if not image.content_type.startswith("image/"):
            return JsonResponse({"error": "Invalid file type."}, status=400)

        extension = image.name.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{extension}"

        save_path = default_storage.save(
            "uploads/" + unique_filename, ContentFile(image.read())
        )
        image_url = settings.MEDIA_URL + save_path

        return JsonResponse({"url": image_url})

    return JsonResponse({"error": "Invalid request"}, status=400)


def index(request):
    blogs = Blog.objects.filter(is_draft=False).order_by("-created_at")
    for blog in blogs:
        blog.author_display_name = blog.author.get_display_name()
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

            if action == "preview":
                # Generate preview content for display on the same page
                raw_html = markdown.markdown(form.cleaned_data["content"])

                allowed_tags = ALLOWED_TAGS.union(
                    {"img", "p", "div", "span", "h1", "h2", "h3", "h4", "h5", "h6"}
                )
                allowed_attributes = {"img": ["src", "alt", "title"]}
                content_html = bleach.clean(
                    raw_html, tags=allowed_tags, attributes=allowed_attributes
                )

                # Render the new page with preview content
                return render(
                    request,
                    "blogs/new.html",
                    {"form": form, "blog": blog, "content_html": content_html},
                )

            elif action == "publish":
                blog.is_draft = False
                blog.save()
                return redirect("blogs:index")

            # Save as draft if no specific action
            blog.is_draft = True
            blog.save()
            return redirect("blogs:index")

        return render(request, "blogs/new.html", {"form": form})

    else:
        form = BlogForm()
    return render(request, "blogs/new.html", {"form": form})


def show(request, pk):
    # Retrieve the blog object or return a 404 error if not found
    blog = get_object_or_404(Blog, pk=pk)

    # Convert the blog content from Markdown to HTML
    raw_html = markdown.markdown(
        blog.content,
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            "markdown.extensions.toc",
            "markdown.extensions.sane_lists",
        ],
    )

    # Convert ALLOWED_TAGS frozenset to a list and add custom tags
    allowed_tags = list(bleach.ALLOWED_TAGS) + [
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "p",
        "ul",
        "ol",
        "li",
        "a",
        "img",
        "pre",
        "code",
        "blockquote",
        "hr",
        "em",
        "strong",
        "br",
    ]
    allowed_attributes = {
        "a": ["href", "title"],
        "img": ["src", "alt", "title"],
        "code": ["class"],  # Allow classes for syntax highlighting
    }
    # Sanitize the HTML using bleach to allow only safe tags and attributes
    content_html = bleach.clean(
        raw_html, tags=allowed_tags, attributes=allowed_attributes
    )

    # Update the views count efficiently
    blog.views += 1
    blog.save(update_fields=["views"])

    # Get the display name of the author
    author_display_name = blog.author.get_display_name()

    # Render the template with the required context
    return render(
        request,
        "blogs/show.html",
        {
            "blog": blog,
            "content_html": content_html,
            "author_display_name": author_display_name,
        },
    )


@login_required
def edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if blog.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this blog post.")

    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            action = request.POST.get("action")

            if action == "update":
                # Save and redirect to the blog's detail page
                blog = form.save()
                return redirect("blogs:show", pk=blog.pk)

            elif action == "save_draft":
                # Save as draft and redirect to user drafts page
                blog = form.save(commit=False)
                blog.is_draft = True  # Set the blog post as a draft
                blog.save()
                return redirect("blogs:user_drafts")  # Redirect to user drafts page

    else:
        form = BlogForm(instance=blog)

    # Initial rendering of the edit page
    return render(request, "blogs/edit.html", {"form": form, "blog": blog})


@login_required
def delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if blog.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this blog post.")

    if request.method == "POST":
        blog.delete()
        return redirect("blogs:index")
    return render(request, "blogs/delete.html", {"blog": blog})
