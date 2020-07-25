from django.views.generic import FormView

from applications.theme.forms.switcher import SwitchThemeForm
from applications.theme.views.mixins import ThemeMixin


class SwitchThemeView(ThemeMixin, FormView):
    http_method_names = ["post"]
    form_class = SwitchThemeForm
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
