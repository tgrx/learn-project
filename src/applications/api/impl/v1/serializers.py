from rest_framework.serializers import ModelSerializer

from applications.blog.models import Tweet
from applications.onboarding.models import Avatar


class AvatarSerializer(ModelSerializer):
    class Meta:
        model = Avatar
        fields = "__all__"


class TweetSerializer(ModelSerializer):
    class Meta:
        model = Tweet
        fields = "__all__"
