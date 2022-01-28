from django.views import View
from django.shortcuts import render

from main.models import Ticket


class Main(View):
    def get(self, request):
        return render(request, 'main_page.html')

class OfferView(View):
    def get(self, request):
        tickets = Ticket.objects.all()

        return render(request, 'offer.html', {'tickets': tickets})