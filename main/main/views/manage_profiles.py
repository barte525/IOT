from django.views import View
from django.shortcuts import redirect
from main.models.users import CardOwner, Seller
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
        return HttpResponse("Card owner View")


class SellerView(View):
    def get(self, request):
        if not Seller.check_permissions(request):
            return HttpResponse("Brak uprawnien")
        return HttpResponse("Seller View")

