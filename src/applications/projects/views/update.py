from django.views.generic import UpdateView

from applications.projects.models import Project
from applications.stats.utils import count_stats


@count_stats
class UpdateProjectView(UpdateView):
    model = Project
    fields = "__all__"
