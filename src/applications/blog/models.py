from datetime import datetime

from django.db import models
from django.urls import reverse_lazy


class Tweet(models.Model):
    created = models.DateTimeField(default=datetime.utcnow, editable=False)
    content = models.TextField()

    def __str__(self) -> str:
        return f"{self.__class__.__name__} #{self.pk} @ {self.created}"

    class Meta:
        ordering = ["-created"]

    def get_absolute_url(self):
        kwargs = {"pk": self.pk}
        return reverse_lazy("blog:tweet", kwargs=kwargs)
