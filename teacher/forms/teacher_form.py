from django import forms

from teacher.models import TeacherInfo


class TeacherInfoForm(forms.ModelForm):
    class Meta:
        model = TeacherInfo
        fields = ["user", "expertise", "introduce"]
        widgets = {
            "introduce": forms.Textarea(
                attrs={
                    "rows": 5,
                    "cols": 40,
                    "placeholder": "自我介紹",
                }
            ),
            "expertise": forms.TextInput(attrs={"placeholder": "填寫專業能力"}),
        }
