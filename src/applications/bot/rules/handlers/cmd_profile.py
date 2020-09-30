from applications.bot.rules.consts import DEFAULT_LOW
from applications.bot.rules.custom_types import MessageT
from applications.bot.rules.utils import get_chance
from applications.bot.rules.utils import get_gamer


def handle_cmd_profile(message: MessageT) -> str:
    gamer, _ = get_gamer(message)

    chance = get_chance(message)

    text_response = (
        f"Границы: {DEFAULT_LOW}..{gamer.high}.\n"
        f"\n"
        f"Шанс: {chance}%.\n"
        f"\n"
        f"Деньги: {gamer.money}$.\n"
    )

    return text_response
