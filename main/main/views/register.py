from django.views import View
from django.shortcuts import render
from main.models.users import Seller
from django.http import HttpResponse
from main.models.users import User, CardOwner
from main.models.card import Card


class RegisterUser(View):
    def get(self, request):
        if not Seller.check_permissions(request):
            return HttpResponse("Brak uprawnien")
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        card_id = request.POST['cardId']
        password = User.generate_random_password(20)
        if User.objects.filter(email=email).exists():
            return HttpResponse("Użytkownik o podanym email juz istnieje.")
        if Card.objects.filter(card_id=card_id).exists():
            return HttpResponse("Karta o podanym id juz istnieje.")
        if len(card_id) < 20 or len(card_id) > 30:
            return HttpResponse("Podane id karty nie spełnia wymagań.")
        user = User.objects.create_user(email=email, password=password, name=name, surname=surname)
        user.save()
        card_user = CardOwner(user=user)
        card_user.save()
        Card(card_id=card_id, user=card_user).save()
        return HttpResponse("Stworzenie użytkownika powiodło się, wygenerowane hasło: " + password)
