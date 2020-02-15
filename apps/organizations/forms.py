from django import forms

from apps.operations.models import UserAsk


class AddAskForm(forms.ModelForm):
    mobile = forms.CharField(max_length=30, min_length=8, required=True)

    class Meta:
        model = UserAsk
        fields = ["mobile", "course_name"]