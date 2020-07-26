from django.urls import path

from applications.stats import views
from applications.stats.apps import StatsConfig

app_name = StatsConfig.label

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("reset/", views.ResetView.as_view(), name="reset"),
]
