from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from applications.projects.models import Project
from applications.stats.utils import count_stats


@count_stats
class SingleProjectView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "projects/single.html"
