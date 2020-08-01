from django.db import models


class Project(models.Model):
    name = models.TextField(unique=True)
    description = models.TextField(null=True, blank=True)
    started = models.DateField(null=True, blank=True)
    ended = models.DateField(null=True, blank=True)
