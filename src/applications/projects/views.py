from django import forms
from django.conf import settings
from django.views.generic import FormView

from applications.projects.models import Project

PROJECTS = settings.REPO_DIR / "projects.json"


class ProjectForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(required=False, widget=forms.Textarea)
    started = forms.DateField()
    ended = forms.DateField(required=False)


class AllProjectsView(FormView):
    template_name = "projects/all_projects.html"
    form_class = ProjectForm
    success_url = "/projects/"

    def form_valid(self, form):
        project = Project(**form.cleaned_data)
        project.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["object_list"] = Project.all()
        return ctx


class SingleProjectView(FormView):
    template_name = "projects/single_project.html"
    form_class = ProjectForm
    success_url = "/projects/"

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        project_id = self.kwargs["project_id"]
        project = Project.one(project_id)
        ctx["object"] = project
        return ctx
