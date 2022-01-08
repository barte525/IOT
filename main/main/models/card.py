from django.db import models
from .users import CardOwner


class Card(models.Model):
    card_id = models.CharField(max_length=30)
    user = models.ForeignKey(CardOwner, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    ticket_expiration_date = models.DateField()
