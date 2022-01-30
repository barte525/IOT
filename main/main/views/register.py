from django.views import View
from django.shortcuts import render, redirect
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
            msgStatus = "Nie udało się"
            msgDesc = "Istnieje już użytkownik o podanym adresie email: " + email
            alertClass = "alert-danger"
            return render(request, 'register_response.html', {'messageStatus': msgStatus, 'messageDesc': msgDesc, 'alertClass': alertClass})
        if Card.objects.filter(card_id=card_id).exists():
            msgStatus = "Nie udało się"
            msgDesc = "Karta o podanym id juz istnieje."
            alertClass = "alert-danger"
            return render(request, 'register_response.html', {'messageStatus': msgStatus, 'messageDesc': msgDesc, 'alertClass': alertClass})
        if len(card_id) < 20 or len(card_id) > 30:
            msgStatus = "Nie udało się"
            msgDesc = "Podane id karty nie spełnia wymagań."
            alertClass = "alert-danger"
            return render(request, 'register_response.html',
                          {'messageStatus': msgStatus, 'messageDesc': msgDesc, 'alertClass': alertClass})
        user = User.objects.create_user(email=email, password=password, name=name, surname=surname)
        user.save()
        card_user = CardOwner(user=user)
        card_user.save()
        Card(card_id=card_id, user=card_user).save()
        msgStatus = "Dodano użytkownika"
        msgDesc = "Stworzenie użytkownika powiodło się, wygenerowane hasło: " + password
        alertClass = "alert-success"
        return render(request, 'register_response.html',
                      {'messageStatus': msgStatus, 'messageDesc': msgDesc, 'alertClass': alertClass})

class RegisterUserResponse(View):
    def get(self, request):
        if not Seller.check_permissions(request):
            return HttpResponse("Brak uprawnien")
        return render(request, 'register_response.html', {'messageStatus': 'Brak próby rejestracji', 'messageDesc': 'Przejdź do rejestracji użyutkownika. W profilu kliknij przycisk Zarejestruj użytkownika karty.', 'alertClass': 'alert-info'})