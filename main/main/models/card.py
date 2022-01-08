from django.db import models
from .users import CardOwner
import uuid


class Card(models.Model):
    card_id = models.CharField(max_length=30)
    user = models.ForeignKey(CardOwner, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    ticket_expiration_date = models.DateField(null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
