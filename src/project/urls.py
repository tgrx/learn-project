from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("applications.target.urls")),
    path("admin/", admin.site.urls),
    path("blog/", include("applications.blog.urls")),
    path("hello/", include("applications.hello.urls")),
    path("o/", include("applications.onboarding.urls")),
    path("pr/", include("applications.pr.urls")),
    path("projects/", include("applications.projects.urls")),
    path("stats/", include("applications.stats.urls")),
    path("theme/", include("applications.theme.urls")),
]
