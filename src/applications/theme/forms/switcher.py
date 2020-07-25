from django import forms


class SwitchThemeForm(forms.Form):
    origin = forms.CharField(widget=forms.HiddenInput)
