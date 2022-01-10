from django.views import View
from django.shortcuts import render, redirect
from main.models.users import Seller
from django.http import HttpResponse


class SellerBuyTicket(View):
    def get(self, request):
        if not Seller.check_permissions(request):
            return HttpResponse("Brak uprawnien")
        return render(request, 'seller_buy_ticket.html')
    def post(self, request):
        if not Seller.check_permissions(request):
            return HttpResponse("Brak uprawnien")

        # add validation - check if cardId is in database
        # example uuid value: c5ecbde1-cbf4-11e5-a759-6096cb89d9a5
        cardId = request.POST.get("cardId")
        ticketId = request.POST.get("ticketId")

        return redirect('/profil/sprzedawca/zakupBiletu/' + cardId + '/' + ticketId)


class SellerBuyTicketSave(View):
    def get(self, request, cardId, ticketId):
        if not Seller.check_permissions(request):
            return HttpResponse("Brak uprawnien")

        return render(request, 'seller_buy_ticket_finalize.html', {'cardId': cardId, 'name': "Jan", 'surname': "Kowalski",
                                                                   'days': '10', 'countedExpDate': '20.04.2022', 'price': '30'})

    def post(self, request, cardId, ticketId):
        pass