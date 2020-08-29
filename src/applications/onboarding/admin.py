from django.contrib import admin
from django.contrib.admin import ModelAdmin

from applications.onboarding.models import Profile


@admin.register(Profile)
class ProfileAdminModel(ModelAdmin):
    pass
