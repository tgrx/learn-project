from django import forms

from applications.blog.models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = [Tweet.content.field.name]
        widgets = {
            Tweet.content.field.name: forms.Textarea(attrs={"cols": 70, "rows": 2}),
        }
        labels = {Tweet.content.field.name: "SayView something:"}
