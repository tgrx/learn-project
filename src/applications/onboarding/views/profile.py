from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

from applications.onboarding.forms import AvatarForm
from applications.onboarding.forms import ProfileForm
from applications.onboarding.mixins import CurrentUserMixin
from applications.onboarding.models import Profile
from applications.stats.utils import count_stats


@count_stats
class ProfileView(CurrentUserMixin, FormMixin, LoginRequiredMixin, DetailView):
    form_class = ProfileForm
    template_name = "onboarding/profile.html"

    def get_initial(self):
        if not self.object:
            return {}

        model_attrs = {Profile.birth_date, Profile.display_name}
        model_fields = {attr.field.name for attr in model_attrs}
        initial = {field: getattr(self.object, field) for field in model_fields}
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["form_avatar"] = AvatarForm()

        return ctx

    def get_object(self, queryset=None):
        return self.get_current_profile()
