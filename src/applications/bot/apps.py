from django.apps import AppConfig


class BotConfig(AppConfig):
    label = "bot"
    name = f"applications.{label}"
