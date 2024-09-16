from django import forms

from .models import Blog  # Import the Blog model


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog  # Model is Blog
        fields = [
            "title",
            "content",
            "category",
            "is_draft",
        ]  # Include 'is_draft' and 'category'
        labels = {
            "title": "標題",
            "content": "內容",
            "category": "類別",  # Label for category
            "is_draft": "儲存為草稿",  # Label for 'is_draft'
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
            "category": forms.Select(
                attrs={
                    "class": "w-full p-2 border-2 border-blue-500 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "id": "id_category",  # ID for the category field
                }
            ),
            "is_draft": forms.CheckboxInput(
                attrs={
                    "class": "w-6 h-6 text-blue-500 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "id": "id_is_draft",  # ID for the is_draft checkbox
                }
            ),
        }
