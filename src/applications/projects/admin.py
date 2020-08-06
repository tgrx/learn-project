from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from applications.projects.models import Project


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(),
        }


@admin.register(Project)
class ProjectAdminModel(ModelAdmin):
    form = ProjectAdminForm
