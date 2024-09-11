from django import forms
from django.core.exceptions import ValidationError

from teachers.models import Teacher


class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = [
            "user",
            "nickname",
            "expertise",
            "introduce",
            "schedule_start",
            "schedule_end",
        ]
        widgets = {
            "nickname": forms.TextInput(attrs={"class": "block w-full p-2"}),
            "introduce": forms.Textarea(
                attrs={
                    "placeholder": "文字內容最少50~最多500",
                    "class": "block w-full p-2",
                }
            ),
            "expertise": forms.TextInput(
                attrs={
                    "placeholder": "Ex:JavaScript..Python..",
                    "class": "block w-full p-2",
                }
            ),
            "schedule_start": forms.DateTimeInput(
                attrs={
                    "placeholder": "開始諮詢時間",
                    "type": "datetime-local",
                    "class": "block px-4 py-2 mt-2 text-gray-800 bg-white border border-gray-300",
                }
            ),
            "schedule_end": forms.DateTimeInput(
                attrs={
                    "placeholder": "結束諮詢時間",
                    "type": "datetime-local",
                    "class": "block px-4 py-2 mt-2 text-gray-800 bg-white border border-gray-300",
                }
            ),
            "user": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].required = False
