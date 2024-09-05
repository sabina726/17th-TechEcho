from django import forms

from teachers.models import TeacherInfo


class TeacherInfoForm(forms.ModelForm):
    class Meta:
        model = TeacherInfo
        fields = ["user", "nickname", "expertise", "introduce", "schedule"]
        widgets = {
            "introduce": forms.Textarea(
                attrs={
                    "rows": 5,
                    "cols": 50,
                    "placeholder": "內文100~500",
                }
            ),
            "expertise": forms.TextInput(
                attrs={
                    "placeholder": "Ex:JavaScript..Python..",
                }
            ),
            "schedule": forms.Textarea(
                attrs={
                    "rows": 3,
                    "cols": 50,
                    "placeholder": "可諮詢時間",
                }
            ),
        }
        labels = {
            "user": "",
            "nickname": "暱稱",
            "expertise": "專業能力",
            "introduce": "自我介紹",
            "schedule": "諮詢時間",
        }
