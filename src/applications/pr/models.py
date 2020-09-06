import itertools
import random
from typing import Tuple
from uuid import uuid4

from django.db import models


def get_random_incides(length, plex) -> Tuple[int]:
    indices = range(length)
    combinations = tuple(itertools.combinations(indices, plex))
    combination = random.choice(combinations)
    shuffled = tuple(sorted(combination, key=lambda i: random.random()))
    return shuffled


class Campaign(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    enabled = models.BooleanField(default=False)
    active_from = models.DateTimeField(null=True, blank=True)
    active_till = models.DateTimeField(null=True, blank=True)
    name = models.TextField()
    celebrity = models.TextField()
    social_platform = models.TextField(null=True, blank=True)
    social_url = models.URLField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    @property
    def random_photos(self):
        photos_all = self.photos.all()
        indices = get_random_incides(len(photos_all), 4)
        photos_random = [photos_all[i] for i in indices]
        return photos_random


class Photo(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="photos"
    )
    url = models.URLField()
