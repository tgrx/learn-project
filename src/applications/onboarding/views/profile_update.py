from django.urls import reverse_lazy
from django.views.generic import UpdateView

from applications.onboarding.forms import ProfileForm
from applications.onboarding.mixins import CurrentUserMixin
from applications.stats.utils import count_stats


@count_stats
class ProfileUpdateView(CurrentUserMixin, UpdateView):
    form_class = ProfileForm
    http_method_names = ["post"]
    success_url = reverse_lazy("onboarding:profile")

    def get_object(self, queryset=None):
        return self.get_current_profile()
