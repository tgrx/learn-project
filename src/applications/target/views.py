from django.views.generic import TemplateView

from applications.stats.utils import count_stats


@count_stats
class IndexView(TemplateView):
    template_name = "target/index.html"
