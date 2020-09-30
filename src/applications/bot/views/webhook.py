import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import Form
from django.urls import reverse_lazy
from django.views.generic import FormView

from applications.bot.rules.consts import TELEGRAM_API
from applications.bot.rules.utils import get_webhook_info


class WebhookView(LoginRequiredMixin, FormView):
    form_class = Form
    success_url = reverse_lazy("bot:manage")
    template_name = "bot/webhook.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["webhook"] = get_webhook_info()
        return ctx

    def form_valid(self, form):
        webhook_path = reverse_lazy("bot:webhook")
        webhook = f"https://{settings.SITE}{webhook_path}"
        payload = {"url": webhook}

        method = f"{TELEGRAM_API}/setWebhook"

        requests.post(method, json=payload)

        return super().form_valid(form)
