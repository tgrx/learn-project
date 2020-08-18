# Generated by Django 3.0.8 on 2020-08-01 10:58

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("started", models.DateField(blank=True, null=True)),
                ("ended", models.DateField(blank=True, null=True)),
            ],
        ),
    ]