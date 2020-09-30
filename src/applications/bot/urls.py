from django.urls import path

from applications.bot.apps import BotConfig
from applications.bot.views import GameView
from applications.bot.views import WebhookView

app_name = BotConfig.label

urlpatterns = [
    path("manage/", WebhookView.as_view(), name="manage"),
    path("webhook/", GameView.as_view(), name="webhook"),
]
