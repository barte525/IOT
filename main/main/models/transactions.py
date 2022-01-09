from django.db import models
from .card import Card
from .tickets import Ticket
import uuid


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateField()
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)