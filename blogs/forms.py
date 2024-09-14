from django import forms

from .models import Blog  # Updated to import the Blog model


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog  # Changed from Article to Blog
        fields = ["title", "content"]
        labels = {
            "title": "標題",
            "content": "內容",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full p-2 border-2 border-blue-500 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "id": "id_title",  # ID for the title field
                    "placeholder": "請輸入標題",  # Placeholder text
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "w-full p-2 border-2 border-blue-500 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "id": "id_content",  # ID for the content field
                    "placeholder": "請輸入內容",  # Placeholder text
                }
            ),
        }
