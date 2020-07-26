from django import forms


class OriginForm(forms.Form):
    origin = forms.CharField(widget=forms.HiddenInput)
