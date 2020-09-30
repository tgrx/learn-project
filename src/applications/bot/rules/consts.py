from django.conf import settings

_bot_token = settings.TELEGRAM_BOT_TOKEN

TELEGRAM_API = f"https://api.telegram.org/bot{_bot_token}"

DEFAULT_LOW = 1
DEFAULT_HIGH = 100
DEFAULT_MONEY = 1000

COST_HIGH_LOWER = 100
COST_ROLL = 1
