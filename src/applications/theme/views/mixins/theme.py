from applications.theme.custom_types import ThemeT
from applications.theme.utils import ThemeManager


class ThemeMixin:
    def get_theme(self) -> ThemeT:
        return ThemeManager.get_theme_from_session(self.request)

    def switch_theme(self) -> None:
        return ThemeManager.switch_theme_within_session(self.request)
