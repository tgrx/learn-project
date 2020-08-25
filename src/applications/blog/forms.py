from django import forms

from applications.blog.models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        fields = [Tweet.content.field.name]
        labels = {Tweet.content.field.name: "What's on your mind?"}
        model = Tweet
        widgets = {
            Tweet.content.field.name: forms.Textarea(attrs={"cols": 70, "rows": 2}),
        }
