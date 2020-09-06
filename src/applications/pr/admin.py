from django.contrib import admin

from .models import Campaign
from .models import Photo


@admin.register(Campaign)
class CampaignAdminModel(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdminModel(admin.ModelAdmin):
    pass
