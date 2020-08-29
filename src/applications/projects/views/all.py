from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from applications.projects.models import Project
from applications.stats.utils import count_stats


@count_stats
class AllProjectsView(LoginRequiredMixin, ListView):
    queryset = Project.objects.filter(visible=True)
    template_name = "projects/all.html"
