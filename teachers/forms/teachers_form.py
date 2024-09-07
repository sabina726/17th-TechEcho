from django import forms

from teachers.models import Teacher


class TeacherInfoForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = ["user", "nickname", "expertise", "introduce", "schedule"]
        widgets = {
            "introduce": forms.Textarea(
                attrs={
                    "placeholder": "文字內容最少50~最多500",
                }
            ),
            "expertise": forms.TextInput(
                attrs={
                    "placeholder": "Ex:JavaScript..Python..",
                }
            ),
            "schedule": forms.TextInput(
                attrs={
                    "placeholder": "可諮詢時間",
                }
            ),
            "user": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].required = False
