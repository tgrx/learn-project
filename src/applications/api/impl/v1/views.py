from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from applications.api.impl.v1.serializers import AvatarSerializer
from applications.api.impl.v1.serializers import TweetSerializer
from applications.blog.models import Tweet
from applications.onboarding.models import Avatar


class AvatarViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = AvatarSerializer
    queryset = Avatar.objects.all()


class TweetViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()
