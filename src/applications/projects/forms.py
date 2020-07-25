from django import forms


class ProjectForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(required=False, widget=forms.Textarea)
    started = forms.DateField()
    ended = forms.DateField(required=False)
