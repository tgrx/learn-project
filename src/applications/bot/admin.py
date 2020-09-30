from django.contrib import admin
from django.contrib.admin import ModelAdmin

from applications.bot.models import Gamer


@admin.register(Gamer)
class GamerAdminModel(ModelAdmin):
    pass
