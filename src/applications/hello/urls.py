from django.urls import path

from applications.hello.apps import HelloConfig
from applications.hello.views import IndexView

app_name = HelloConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
