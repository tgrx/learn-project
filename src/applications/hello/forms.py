from django import forms


class HelloForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    age = forms.IntegerField(required=False)
