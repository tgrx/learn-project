from applications.bot.rules.consts import COST_HIGH_LOWER
from applications.bot.rules.consts import DEFAULT_LOW
from applications.bot.rules.custom_types import MessageT
from applications.bot.rules.utils import get_chance
from applications.bot.rules.utils import get_gamer
from applications.bot.rules.utils import get_high

from .cmd_profile import handle_cmd_profile


def handle_cmd_set_high(message: MessageT) -> str:
    gamer, _ = get_gamer(message)
    gamer.need_new_high = True
    gamer.save()

    chance = get_chance(message)

    text_response = (
        f"Текущий диапазон: {DEFAULT_LOW}..{gamer.high}\n"
        f"Шанс: {chance}%\n"
        f"\n"
        f"Понижаешь границу - понижаем твои деньги на ${COST_HIGH_LOWER}.\n"
        f"\n"
        f"Присылай новую границу!"
    )

    return text_response


def handle_cmd_set_high_update(message: MessageT) -> str:
    new_high = get_high(message)
    gamer, _ = get_gamer(message)

    if new_high <= DEFAULT_LOW:
        text_response = (
            f"{new_high}? Ну и граница.\n" f"Задай нормальную, не будь это самое!"
        )
        return text_response

    lower_the_high = int(new_high < gamer.high)

    if lower_the_high and gamer.money < COST_HIGH_LOWER:
        text_response = (
            f"Денег у тебя не хватает границу понизить.\n"
            f"\n"
            f"Это стоит: ${COST_HIGH_LOWER}.\n"
            f"У тебя: ${gamer.money}.\n"
            f"\n"
            f"Можешь только повышать ставки."
        )
        return text_response

    cost = COST_HIGH_LOWER * lower_the_high

    gamer.high = new_high
    gamer.need_new_high = False
    gamer.money -= cost
    gamer.save()

    profile = handle_cmd_profile(message)

    text_response = (
        f"Новые данные!\n" f"\n" f"{profile}" f"\n" f"Теперь Игра возобновляется."
    )

    return text_response
