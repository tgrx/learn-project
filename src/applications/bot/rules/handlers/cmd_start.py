from applications.bot.rules.custom_types import MessageT
from applications.bot.rules.utils import get_gamer


def handle_cmd_start(message: MessageT) -> str:
    gamer, _ = get_gamer(message)

    text_response = (
        f"Милости прошу к нашему шалашу!\n"
        f"\n"
        f"Ты зареган под номером {gamer.pk}.\n"
        f"На твоём балансе ${gamer.money or 0}.\n"
        f"\n"
        f"угадай число от 1 до {gamer.high}\n"
    )

    return text_response
