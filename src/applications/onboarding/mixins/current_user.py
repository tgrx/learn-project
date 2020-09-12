from typing import Optional

from django.contrib.auth import get_user_model

from applications.onboarding.models import Avatar
from applications.onboarding.models import Profile

User = get_user_model()


class CurrentUserMixin:
    def get_current_user(self) -> User:
        return self.request.user

    def get_current_profile(self) -> Optional[Profile]:
        profile = None
        exc_missing = (User.profile.RelatedObjectDoesNotExist,)
        try:
            profile = self.request.user.profile
        except exc_missing:
            pass
        return profile

    def setup_profile(self):
        profile = self.get_current_profile()
        if not profile:
            profile = Profile(user=self.get_current_user())
            profile.save()

    def get_current_avatar(self) -> Optional[Avatar]:
        avatar = None
        exc_missing = (
            User.profile.RelatedObjectDoesNotExist,
            Profile.avatar.RelatedObjectDoesNotExist,
        )
        try:
            avatar = self.request.user.profile.avatar
        except exc_missing:
            pass
        return avatar
