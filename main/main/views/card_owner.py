from django.views import View
from django.shortcuts import render, redirect
from main.models.users import CardOwner
from main.models.tickets import Ticket
from django.http import HttpResponse


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


        return render(request, 'card_owner_ticket.html')


class CardOwnerBuyTicketView(View):
    def get(self, request):
        if not CardOwner.check_permissions(request):
            return HttpResponse("Brak uprawnien")


        return render(request, 'card_owner_buy_ticket.html')
