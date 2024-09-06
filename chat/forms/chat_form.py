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
                    "placeholder": "Add message ...",
                    "maxlength": "300",
                    "autofocus": True,
                }
            )
        }
