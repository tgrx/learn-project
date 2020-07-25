from typing import Dict

from django.http import HttpRequest

from applications.theme.utils import ThemeManager


def theme(request: HttpRequest) -> Dict:
    theme = ThemeManager.get_theme_from_session(request)
    theme_next = ThemeManager.get_next_theme(theme)

    return {
        "theme": theme,
        "theme_next": theme_next,
    }
