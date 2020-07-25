from django.urls import reverse_lazy
from django.views.generic import RedirectView

from applications.projects.models import Project
from applications.projects.views.mixins import SingleObjectMixin


class DeleteProjectView(SingleObjectMixin, RedirectView):
    http_method_names = ["post"]
    model = Project
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        project = self.get_object()
        project.delete()

        return reverse_lazy("projects:all")
