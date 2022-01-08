from django.db import models


class Ticket(models.Model):
    days_amount = models.IntegerField()
    price = models.FloatField()

    @staticmethod
    def create_tickets():
        Ticket(days_amount=7, price=30.0).save()
        Ticket(days_amount=14, price=50.0).save()
        Ticket(days_amount=30, price=80.0).save()
        Ticket(days_amount=60, price=140.0).save()
        Ticket(days_amount=90, price=200.0).save()
        Ticket(days_amount=180, price=350.0).save()
