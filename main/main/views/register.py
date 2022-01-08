from django.views import View
from django.shortcuts import render
from main.models.users import Seller
from django.http import HttpResponse


class RegisterUser(View):
    def get(self, request):
        if not Seller.check_permissions(request):
            return HttpResponse("Brak uprawnien")
        return render(request, 'register.html')