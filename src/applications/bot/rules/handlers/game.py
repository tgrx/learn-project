from random import randint

from applications.bot.rules.consts import COST_ROLL
from applications.bot.rules.consts import DEFAULT_LOW
from applications.bot.rules.custom_types import MessageT
from applications.bot.rules.utils import get_chance
from applications.bot.rules.utils import get_gamer


def handle_game(message: MessageT) -> str:
    gamer, _ = get_gamer(message)
    chance = get_chance(message)

    if gamer.debtor:
        text_response = (
            f"! ! !\n"
            f"\n"
            f"Баланс: {gamer.money}$.\n"
            f"Sorry, но ты торчишь денег.\n"
            f"\n"
            f"Какое играть?"
        )
        return text_response

    try:
        number_guess = int(message.text)
    except ValueError:
        cost = -COST_ROLL * 10
        text_response = f"Ну и что ты вводишь вообще? {cost}$ за такое."
        gamer.pay(cost)
        return text_response

    number_fortune = randint(DEFAULT_LOW, gamer.high)

    win = bool(number_guess == number_fortune)

    cost = {
        False: -chance * COST_ROLL,
        True: (100 - chance) * COST_ROLL,
    }[win]
    cost = round(cost, 2)

    gamer.pay(cost)

    text_response = {
        False: f"Лох. {cost}$. Играй дальше :)",
        True: f"ЕЕЕ УДАЧА! +${cost}! Играем ещё?!",
    }[win]

    return text_response
