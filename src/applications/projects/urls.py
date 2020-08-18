from django.urls import path

from applications.projects import views
from applications.projects.apps import ProjectsConfig

app_name = ProjectsConfig.label

urlpatterns = [
    path("", views.AllProjectsView.as_view(), name="all"),
    path("add/", views.AddProjectView.as_view(), name="add"),
    path("p/<str:pk>/", views.SingleProjectView.as_view(), name="single"),
    path("p/<str:pk>/delete/", views.DeleteProjectView.as_view(), name="delete"),
    path("p/<str:pk>/update/", views.UpdateProjectView.as_view(), name="update"),
]
