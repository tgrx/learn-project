# Generated by Django 3.1 on 2020-08-22 08:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("stats", "0002_auto_20200804_1828"),
    ]

    operations = [
        migrations.AlterModelOptions(name="visit", options={"ordering": ["-at"]},),
    ]
