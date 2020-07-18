from django.contrib import admin
from django.urls import path

from project.views import handle_goodbye
from project.views import handle_hello
from project.views import handle_lesson
from project.views import handle_projects

urlpatterns = [
    path("admin/", admin.site.urls),
    path("css/", handle_lesson),
    path("goodbye/", handle_goodbye),
    path("hello/", handle_hello),
    path("projects/", handle_projects),
    path("projects/<str:project_id>/", handle_projects),
]
