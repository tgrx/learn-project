from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from applications.projects.models import Project
from applications.stats.utils import count_stats


@count_stats
class UpdateProjectView(LoginRequiredMixin, UpdateView):
    fields = "__all__"
    model = Project
