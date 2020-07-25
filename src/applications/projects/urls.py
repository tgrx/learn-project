from django.urls import path

from applications.projects import views
from applications.projects.apps import ProjectsConfig

app_name = ProjectsConfig.label

urlpatterns = [
    path("", views.AllProjectsView.as_view(), name="all"),
    path("<str:pk>/", views.SingleProjectView.as_view(), name="single"),
    path("<str:pk>/delete/", views.DeleteProjectView.as_view(), name="delete",),
]
