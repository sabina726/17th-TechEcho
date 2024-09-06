from django import forms
from django.forms import ModelForm

from chat.models import GroupMessage


class ChatMessageForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ["content"]
        widgets = {
            "content": forms.TextInput(
                attrs={
                    "placeholder": "等待訊息中...",
                    "maxlength": "300",
                    "autofocus": True,
                    "class": "input input-md input-bordered",
                }
            )
        }
        labels = {"content": "訊息"}
