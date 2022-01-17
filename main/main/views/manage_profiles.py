from django.views import View
from django.shortcuts import redirect, render
from main.models.users import CardOwner, Seller, User
from django.http import HttpResponse


class ManageProfiles(View):
    def get(self, request):
        current_ID = request.user.id
        if CardOwner.objects.filter(user=current_ID).exists():
            return redirect('/profil/uzytkownikKarty')
        if Seller.objects.filter(user=current_ID).exists():
            return redirect('/profil/sprzedawca')
        else:
            return HttpResponse("Account is not seller nor cardOwner account")


class CardOwnerView(View):
    def get(self, request):
        if not CardOwner.check_permissions(request):
            return HttpResponse("Brak uprawnien")
        if CardOwner.objects.get(user=request.user.id).force_password_change_check():
            return redirect('/profil/zmianaHasla/')

        current_ID = request.user.id
        user = User.objects.get(id=current_ID)
        name = user.name
        surname = user.surname

        return render(request, 'card_owner_profile.html', {'name': name, 'surname': surname})


class SellerView(View):
    def get(self, request):
        if not Seller.check_permissions(request):
            return HttpResponse("Brak uprawnien")

        current_ID = request.user.id
        user = User.objects.get(id=current_ID)
        name = user.name
        surname = user.surname

        return render(request, 'seller_profile.html', {'name': name, 'surname': surname})

