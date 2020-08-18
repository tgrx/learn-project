from django.urls import reverse_lazy
from django.views.generic import DeleteView

from applications.projects.models import Project
from applications.stats.utils import count_stats


@count_stats
class DeleteProjectView(DeleteView):
    model = Project
    success_url = reverse_lazy("projects:all")
