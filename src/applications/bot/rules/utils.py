from decimal import Decimal
from typing import Optional
from typing import Tuple

import requests

from applications.bot.models import Gamer
from applications.bot.rules.consts import DEFAULT_HIGH
from applications.bot.rules.consts import DEFAULT_LOW
from applications.bot.rules.consts import DEFAULT_MONEY
from applications.bot.rules.consts import TELEGRAM_API
from applications.bot.rules.custom_types import MessageT
from applications.bot.rules.custom_types import WebhookT


def get_gamer(message: MessageT) -> Tuple[Gamer, bool]:
    gamer, created = Gamer.objects.get_or_create(chat_id=message.chat_id)
    if created:
        gamer.high = DEFAULT_HIGH
        gamer.money = DEFAULT_MONEY
        gamer.save()

    return gamer, created


def respond_to_telegram(chat_id: str, message: str) -> None:
    method = f"{TELEGRAM_API}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
    }

    requests.post(method, json=payload)


def get_high(message: MessageT) -> int:
    if not message.text.isdigit():
        return DEFAULT_HIGH
    high = int(message.text)
    return high


def get_chance(message: MessageT) -> Decimal:
    gamer, _ = get_gamer(message)

    chance = Decimal(100) / Decimal(gamer.high - DEFAULT_LOW + 1)
    accuracy = 0 if chance >= 4 else 2
    chance = round(chance, accuracy)

    return chance


def get_webhook_info() -> Optional[WebhookT]:
    method = f"{TELEGRAM_API}/getWebhookInfo"
    response = requests.post(method)
    if response.status_code != 200:
        return None

    payload = response.json()
    ok = payload.get("ok")
    if not ok:
        return None
    result = payload.get("result")
    if not result:
        return None

    kwargs = {attr: result.get(attr) for attr in WebhookT.__annotations__}

    webhook = WebhookT(**kwargs)
    return webhook
