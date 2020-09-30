from django.db import models


class Gamer(models.Model):
    chat_id = models.TextField(unique=True)
    high = models.IntegerField(null=True, blank=True)
    money = models.DecimalField(null=True, blank=True, max_digits=26, decimal_places=2)
    need_new_high = models.BooleanField(default=False)

    def pay(self, cost):
        self.money += cost
        self.save()

    @property
    def debtor(self):
        return bool(self.money < 0)
