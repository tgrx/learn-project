from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import RedirectView

from applications.stats.models import Visit
from applications.stats.utils import count_stats
from applications.stats.utils import generate_dashboard


@count_stats
class IndexView(LoginRequiredMixin, ListView):
    model = Visit
    template_name = "stats/index.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["dashboard"] = generate_dashboard()
        return ctx


class ResetView(LoginRequiredMixin, RedirectView):
    http_method_names = ["post"]

    def get_redirect_url(self, *args, **kwargs):
        Visit.objects.all().delete()
        return reverse_lazy("stats:index")
