from django import forms

from applications.onboarding.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            attr.field.name for attr in (Profile.birth_date, Profile.display_name,)
        ]
