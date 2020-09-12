from django.urls import reverse_lazy
from django.views.generic import UpdateView

from applications.onboarding.forms import AvatarForm
from applications.onboarding.mixins import CurrentUserMixin
from applications.stats.utils import count_stats


@count_stats
class AvatarUpdateView(CurrentUserMixin, UpdateView):
    form_class = AvatarForm
    http_method_names = ["post"]
    success_url = reverse_lazy("onboarding:profile")

    def get_object(self, queryset=None):
        return self.get_current_avatar()

    def form_valid(self, form):
        self.setup_profile()
        return super().form_valid(form)
