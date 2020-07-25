from django.urls import reverse_lazy
from django.views.generic import FormView

from applications.projects.forms import ProjectForm
from applications.projects.models import Project
from applications.projects.views.mixins import SingleObjectMixin


class SingleProjectView(SingleObjectMixin, FormView):
    form_class = ProjectForm
    model = Project
    template_name = "projects/single.html"

    def get_initial(self):
        dct = self.get_object_dct()
        self.shadow_pk(dct)
        return dct

    def get_success_url(self):
        project_id = self.get_object_id()
        kwargs = {"pk": project_id}
        url = reverse_lazy("projects:single", kwargs=kwargs)
        return url

    def form_valid(self, form):
        project = self.get_object()
        self.update_object(project, form)
        project.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        project = self.get_object()
        ctx["object"] = project
        return ctx
