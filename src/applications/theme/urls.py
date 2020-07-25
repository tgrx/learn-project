from django.urls import path

from applications.theme import views
from applications.theme.apps import ThemeConfig

app_name = ThemeConfig.label

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("switch/", views.SwitchThemeView.as_view(), name="switch"),
]
