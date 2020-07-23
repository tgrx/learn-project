from django.urls import path

from .apps import GoodbyeConfig
from .views import GoodbyeView

app_name = GoodbyeConfig.label

urlpatterns = [
    path("", GoodbyeView.as_view(), name="xxx"),
]
