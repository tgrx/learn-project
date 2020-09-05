from django import forms

from applications.onboarding.models import Avatar


class AvatarForm(forms.ModelForm):
    original = forms.FileField(label="Avatar")

    class Meta:
        model = Avatar
        fields = [attr.field.name for attr in (Avatar.original,)]
