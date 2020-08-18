from django.views.generic import CreateView

from applications.projects.models import Project
from applications.stats.utils import count_stats


@count_stats
class AddProjectView(CreateView):
    model = Project
    fields = "__all__"
