from applications.target.apps import TargetConfig
from applications.target.views import IndexView
from django.urls import path

app_name = TargetConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
