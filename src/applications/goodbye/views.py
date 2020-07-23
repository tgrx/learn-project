from random import choice

from django.views.generic import TemplateView


class GoodbyeView(TemplateView):
    template_name = "goodbye/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        tod = choice(("dias", "noches"))

        ctx.update(
            {"tod": tod,}
        )

        return ctx
