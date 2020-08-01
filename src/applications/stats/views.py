from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from applications.stats.models import Visit
from applications.stats.utils import count_stats


@count_stats
class IndexView(TemplateView):
    template_name = "stats/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["object_list"] = Visit.objects.order_by("-at").all()
        ctx["dashboard"] = Visit.generate_dashboard()

        return ctx


class ResetView(RedirectView):
    http_method_names = ["post"]

    def get_redirect_url(self, *args, **kwargs):
        Visit.objects.all().delete()
        return reverse_lazy("stats:index")
