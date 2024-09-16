from django import forms

from teachers.models import Teacher


class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = [
            "introduce",
        ]
        widgets = {
            "introduce": forms.Textarea(
                attrs={
                    "placeholder": "文字內容最少50~最多500",
                    "class": "block w-full p-2 border border-sky-800 rounded-lg indent-2 bg-gray-300",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        # Retrieve the current request user
        self.request_user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
