from django.views.generic import ListView

from applications.projects.models import Project
from applications.stats.utils import count_stats


@count_stats
class AllProjectsView(ListView):
    template_name = "projects/all.html"
    queryset = Project.objects.filter(visible=True)
