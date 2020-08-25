from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from applications.blog.models import Tweet


class TweetAdminForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"style": "width: 400px"}),
        }


@admin.register(Tweet)
class TweetAdminModel(ModelAdmin):
    form = TweetAdminForm
