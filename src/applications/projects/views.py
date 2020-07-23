from dataclasses import asdict

from django import forms
from django.views.generic import FormView
from django.views.generic import RedirectView

from applications.projects.models import Project


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


class SingleObjectMixin:
    model = None

    def get_object_id(self):
        return self.kwargs["project_id"]

    def get_object(self):
        object_id = self.get_object_id()
        return self.model.one(object_id)


class SingleProjectView(SingleObjectMixin, FormView):
    model = Project
    template_name = "projects/single_project.html"
    form_class = ProjectForm
    success_url = "/projects/"

    def get_initial(self):
        project = self.get_object()
        dct = asdict(project)
        try:
            del dct["pk"]
        except KeyError:
            pass
        return dct

    def get_success_url(self):
        project_id = self.get_object_id()
        return f"/projects/{project_id}/"

    def form_valid(self, form):
        project = self.get_object()
        for attr, value in form.cleaned_data.items():
            setattr(project, attr, value)
        project.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        project = self.get_object()
        ctx["object"] = project
        return ctx


class DeleteProjectView(SingleObjectMixin, RedirectView):
    model = Project
    permanent = True
    http_method_names = ["post"]

    def get_redirect_url(self, *args, **kwargs):
        project = self.get_object()
        project.delete()

        return "/projects/"
