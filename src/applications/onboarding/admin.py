from django.contrib import admin
from django.contrib.admin import ModelAdmin

from applications.onboarding.models import Avatar
from applications.onboarding.models import Profile


@admin.register(Profile)
class ProfileAdminModel(ModelAdmin):
    pass


@admin.register(Avatar)
class AvatarAdminModel(ModelAdmin):
    pass
