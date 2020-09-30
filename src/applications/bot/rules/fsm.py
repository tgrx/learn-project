from typing import Callable

from applications.bot.rules import handlers
from applications.bot.rules.custom_types import MessageT
from applications.bot.rules.utils import get_gamer


def get_handler(message: MessageT) -> Callable:
    gamer, _ = get_gamer(message)

    default_handler = {
        False: handlers.handle_game,
        True: handlers.handle_cmd_set_high_update,
    }[gamer.need_new_high]

    routes = {
        "/profile": handlers.handle_cmd_profile,
        "/start": handlers.handle_cmd_start,
        "/set_high": handlers.handle_cmd_set_high,
    }

    handler = routes.get(message.text, default_handler)

    return handler
