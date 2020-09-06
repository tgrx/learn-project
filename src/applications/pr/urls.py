from django.urls import path

from applications.pr.apps import PrConfig
from applications.pr.views import IndexView

app_name = PrConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
