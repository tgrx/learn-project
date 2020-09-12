from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from applications.api.impl.v1.views import AvatarViewSet
from applications.api.impl.v1.views import TweetViewSet

router = DefaultRouter()
router.register("avatar", AvatarViewSet, "avatar")
router.register("tweet", TweetViewSet, "tweet")

urlpatterns = [
    path("", include(router.urls)),
]
