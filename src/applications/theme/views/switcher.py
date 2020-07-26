from django.views.generic import FormView

from applications.stats.utils import count_stats
from applications.theme.views.mixins import ThemeMixin
from project.forms.origin import OriginForm


@count_stats
class SwitchThemeView(ThemeMixin, FormView):
    http_method_names = ["post"]
    form_class = OriginForm
    template_name = "theme/index.html"

    def __init__(self):
        super().__init__()
        self.__origin = None

    def form_valid(self, form):
        self.switch_theme()
        self.__origin = form.cleaned_data["origin"]
        return super().form_valid(form)

    def get_success_url(self):
        return self.__origin
