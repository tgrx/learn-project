from django.urls import reverse_lazy
from django.views.generic import FormView

from applications.projects.forms import ProjectForm
from applications.projects.models import Project


class AllProjectsView(FormView):
    template_name = "projects/all.html"
    form_class = ProjectForm
    success_url = reverse_lazy("projects:all")

    def form_valid(self, form):
        project = Project(**form.cleaned_data)
        project.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["object_list"] = Project.all()
        return ctx
