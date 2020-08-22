from django.db import models


class Visit(models.Model):
    at = models.DateTimeField(null=True, blank=True)
    cl = models.PositiveIntegerField(null=True, blank=True)
    code = models.PositiveIntegerField(null=True, blank=True)
    method = models.TextField(null=True, blank=True)
    tm = models.FloatField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ["-at"]

    def __str__(self):
        return f"Visit(at={self.at}, url={self.url})"

    __repr__ = __str__
