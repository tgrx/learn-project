from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("applications.target.urls")),
    path("admin/", admin.site.urls),
    path("theme/", include("applications.theme.urls")),
    path("hello/", include("applications.hello.urls")),
    path("projects/", include("applications.projects.urls")),
]
