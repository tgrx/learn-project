from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from applications.projects.models import Project
from applications.stats.utils import count_stats


@count_stats
class AddProjectView(LoginRequiredMixin, CreateView):
    fields = "__all__"
    model = Project
