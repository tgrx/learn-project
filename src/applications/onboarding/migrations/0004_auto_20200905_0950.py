# Generated by Django 3.1.1 on 2020-09-05 09:50

import storages.backends.s3boto3
from django.db import migrations
from django.db import models

import applications.onboarding.models.avatar


class Migration(migrations.Migration):
    dependencies = [
        ("onboarding", "0003_auto_20200905_0948"),
    ]

    operations = [
        migrations.AlterField(
            model_name="avatar",
            name="original",
            field=models.FileField(
                blank=True,
                null=True,
                storage=storages.backends.s3boto3.S3Boto3Storage(),
                upload_to=applications.onboarding.models.avatar.upload_to,
            ),
        ),
    ]