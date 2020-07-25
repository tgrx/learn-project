from django.views.generic import TemplateView

from applications.theme.custom_types import ThemeT
from applications.theme.views.mixins import ThemeMixin


class IndexView(ThemeMixin, TemplateView):
    template_name = "theme/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        fsm = {
            ThemeT.BRIGHT: "dias",
            ThemeT.DARK: "noches",
        }
        tod = fsm[self.get_theme()]
        ctx.update({"tod": tod})

        return ctx
