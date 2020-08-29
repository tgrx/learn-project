from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    birth_date = models.DateField(null=True, blank=True)
    display_name = models.TextField(null=True, blank=True)
