from django.views import View
from django.shortcuts import render, redirect
from main.models.users import Seller
from django.http import HttpResponse
from main.models.tickets import Ticket
from main.models.card import Card
from main.models.transactions import Transaction


class SellerBuyTicket(View):
    def get(self, request):
        if not Seller.check_permissions(request):
            return HttpResponse("Brak uprawnien")
        tickets = list(Ticket.objects.all())
        return render(request, 'seller_buy_ticket.html', {'tickets': tickets})

    def post(self, request):
        if not Seller.check_permissions(request):
            return HttpResponse("Brak uprawnien")
        cardId = request.POST.get("cardId")
        ticketId = request.POST.get("ticketId")
        return redirect('/profil/sprzedawca/zakupBiletu/' + cardId + '/' + ticketId)


class SellerBuyTicketSave(View):
    def get(self, request, cardId, ticketId):
        if not Seller.check_permissions(request):
            return HttpResponse("Brak uprawnien")
        if not Card.objects.filter(card_id=cardId).exists():
            return HttpResponse("Karta o podanym id nie istnieje")
        if not Ticket.objects.filter(id=ticketId).exists():
            return HttpResponse("Bilet o podanym uuid nie istnieje")
        card = Card.objects.get(card_id=cardId)
        ticket = Ticket.objects.get(id=ticketId)
        name = card.user.user.name
        surname = card.user.user.surname
        days = ticket.days_amount
        price = ticket.price
        counted_exp_date = card.count_ticket_expiration_date(ticket)
        counted_exp_date_formatted = counted_exp_date.strftime("%d.%m.%Y")
        return render(request, 'seller_buy_ticket_finalize.html', {'cardId': cardId, 'name': name, 'surname': surname,
                                                                   'days': days, 'countedExpDate': counted_exp_date_formatted,
                                                                   'price': price})

    def post(self, request, cardId, ticketId):
        if not Seller.check_permissions(request):
            return HttpResponse("Brak uprawnien")
        if not Card.objects.filter(card_id=cardId).exists():
            return HttpResponse("Karta o podanym id nie istnieje")
        if not Ticket.objects.filter(id=ticketId).exists():
            return HttpResponse("Bilet o podanym uuid nie istnieje")

        card = Card.objects.get(card_id=cardId)
        ticket = Ticket.objects.get(id=ticketId)
        new_exp_date = card.count_ticket_expiration_date(ticket)
        transaction = Transaction.objects.create(card=card, date=new_exp_date, ticket=ticket)
        transaction.save()
        card.ticket_expiration_date = new_exp_date
        card.save()
        days_amount = ticket.days_amount
        new_exp_date_formatted = new_exp_date.strftime("%d.%m.%Y")
        return render(request, 'seller_buy_ticket_success.html', {'daysAmount': days_amount, 'newExpDate': new_exp_date_formatted})