from datetime import date, timedelta, datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.db import transaction

from main.models import CardOwner, Ticket, Card, Transaction


class CardOwnerOfferView(View):
    def get(self, request):
        if not CardOwner.check_permissions(request):
            return HttpResponse("Brak uprawnien")

        tickets = Ticket.objects.all()

        return render(request, 'card_owner_offer.html', {'tickets': tickets})


class CardOwnerStatusView(View):
    def get(self, request):
        if not CardOwner.check_permissions(request):
            return HttpResponse("Brak uprawnien")

        card = Card.objects.get(user__user__id=request.user.id)

        card_owner = CardOwner.objects.get(user_id=request.user.id)

        return render(request, 'card_owner_ticket.html', {'card':card, 'card_owner':card_owner})


class CardOwnerBuyTicketView(View):
    def get(self, request, ticket_id):
        if not CardOwner.check_permissions(request):
            return HttpResponse("Brak uprawnien")
        ticket = Ticket.objects.get(id=ticket_id)
        card = Card.objects.get(user__user__id=request.user.id)
        start_day = date.today() \
            if card.ticket_expiration_date is None \
            else card.ticket_expiration_date + timedelta(days=1)

        card.ticket_expiration_date = card.count_ticket_expiration_date(ticket)
        return render(request, 'card_owner_buy_ticket.html', {"ticket": ticket, "card": card, "start_day": start_day})


class CardOwnerConfirmBuyTicketView(View):
    def get(self, request, trans_id):
        buy_transaction = Transaction.objects.get(id=trans_id)

        return render(request, 'card_owner_confirm_buy_ticket.html',
                      {"success": True, 'new_exp_date': buy_transaction.card.ticket_expiration_date,
                       'trans_id': buy_transaction.id})

    def post(self, request):
        ticket = Ticket.objects.get(id=request.POST['ticket_id'])
        card = Card.objects.get(id=request.POST['card_id'])

        with transaction.atomic():
            card.ticket_expiration_date = card.count_ticket_expiration_date(ticket)
            buy_transaction = Transaction.objects.create(card=card, date=datetime.now(), ticket=ticket)
            card.save()
            buy_transaction.save()

        return render(request, 'card_owner_confirm_buy_ticket.html', {'trans_id': buy_transaction.id})
