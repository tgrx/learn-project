from delorean import Delorean
from django.db.models import Q
from django.views.generic import DetailView

from applications.pr.models import Campaign
from applications.stats.utils import count_stats


@count_stats
class IndexView(DetailView):
    template_name = "pr/index.html"

    def get_object(self, *_a, **_kw):
        atm = Delorean().datetime

        where = (
            (Q(active_from__lte=atm) | Q(active_from__isnull=True))
            & (Q(active_till__gte=atm) | Q(active_till__isnull=True))
            & Q(enabled=True)
        )
        query = Campaign.objects.filter(where)
        obj = query.first()
        return obj
