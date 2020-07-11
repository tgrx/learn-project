from django.contrib import admin
from django.urls import path

from project.views import handle_goodbye
from project.views import handle_projects

urlpatterns = [
    path('admin/', admin.site.urls),
    path('goodbye/', handle_goodbye),
    path('projects/', handle_projects),
    path('projects/<str:project_id>/', handle_projects),
]
