from django.conf import settings
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage


def upload_to(instance: "Avatar", filename):
    return f"{settings.AWS_S3_LOCATION}/avatars/{instance.pk}/{filename}"


class Avatar(models.Model):
    profile = models.OneToOneField(
        "Profile", on_delete=models.CASCADE, primary_key=True
    )
    original = models.FileField(
        storage=S3Boto3Storage(), upload_to=upload_to, null=True, blank=True
    )

    def __str__(self):
        msg = f"{self.profile}"
        return msg
