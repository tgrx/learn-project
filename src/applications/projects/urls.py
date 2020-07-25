from django.urls import path

from applications.projects.apps import ProjectsConfig
from applications.projects.views import AllProjectsView
from applications.projects.views import DeleteProjectView
from applications.projects.views import SingleProjectView

app_name = ProjectsConfig.label

urlpatterns = [
    path("bcv/", AllProjectsView.as_view(), name="all_projects"),
    path("bcv/<str:project_id>/", SingleProjectView.as_view(), name="single_project"),
    path(
        "bcv/<str:project_id>/delete/",
        DeleteProjectView.as_view(),
        name="delete_project",
    ),
]
