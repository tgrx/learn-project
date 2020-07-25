from django.http import HttpRequest

from applications.theme.custom_types import ThemeT


class ThemeManager:
    THEME_SESSION_KEY = "theme"

    @classmethod
    def get_theme_from_session(cls, request: HttpRequest) -> ThemeT:
        theme_value = request.session.get(cls.THEME_SESSION_KEY, ThemeT.BRIGHT.value)
        theme = ThemeT(theme_value)
        return theme

    @classmethod
    def get_next_theme(cls, theme: ThemeT) -> ThemeT:
        fsm = {
            ThemeT.BRIGHT: ThemeT.DARK,
            ThemeT.DARK: ThemeT.BRIGHT,
        }
        next_theme = fsm[theme]
        return next_theme

    @classmethod
    def switch_theme_within_session(cls, request: HttpRequest) -> None:
        current_theme = cls.get_theme_from_session(request)
        next_theme = cls.get_next_theme(current_theme)
        request.session[cls.THEME_SESSION_KEY] = next_theme.value
