from django.db import models
from .card import Card


class Transaction(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateField()
    expiration_date = models.DateField()
