from django.db import models
from .users import CardOwner
import uuid
from datetime import timedelta, date

class Card(models.Model):
    card_id = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(CardOwner, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    ticket_expiration_date = models.DateField(null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def count_ticket_expiration_date(self, ticket):
        exp_date = self.ticket_expiration_date
        if not exp_date or exp_date < date.today():
            exp_date = date.today() + timedelta(days=ticket.days_amount - 1)
        else:
            exp_date += timedelta(days=ticket.days_amount)
        return exp_date
