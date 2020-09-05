from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage


class Avatar(models.Model):
    profile = models.OneToOneField(
        "Profile", on_delete=models.CASCADE, primary_key=True
    )
    original = models.FileField(storage=S3Boto3Storage(), upload_to="avatars")

    def __str__(self):
        msg = f"{self.profile}"
        return msg
