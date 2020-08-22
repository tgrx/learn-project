from django.db import models
from django.urls import reverse_lazy


class Project(models.Model):
    name = models.TextField(unique=True)
    search_name = models.TextField(null=True, blank=True, editable=False)
    description = models.TextField(null=True, blank=True)
    started = models.DateField(null=True, blank=True)
    ended = models.DateField(null=True, blank=True)
    visible = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name} ({self.pk})"

    def get_absolute_url(self):
        kwargs = {"pk": self.pk}
        return reverse_lazy("projects:single", kwargs=kwargs)

    def save(self, *a, **kw):
        super().save(*a, **kw)
        self.search_name = self.normalize(self.name)
        super().save(*a, **kw)

    @staticmethod
    def normalize(name):
        translation_map = {
            "ü": "u",
            "ä": "a",
            "ß": "ss",
        }

        translation = str.maketrans(translation_map)

        name = name.lower().translate(translation)
        return name
