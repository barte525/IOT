from django.views import View
from django.shortcuts import redirect
from main.models.users import CardOwner, Seller
from django.http import HttpResponse


class ManageProfiles(View):
    def get(self, request):
        current_ID = request.user.id
        if CardOwner.objects.filter(user=current_ID).exists():
            return redirect('/profile/cardOwner')
        if Seller.objects.filter(user=current_ID).exists():
            return redirect('/profile/seller')
        else:
            return HttpResponse("Account is not seller nor cardOwner account")


class CardOwnerView(View):
    def get(self, request):
        try:
            user = CardOwner.objects.get(user=request.user.id)
        except CardOwner.DoesNotExist:
            return HttpResponse("Brak uprawnien")
        if user.force_password_change_check():
            return redirect('/profile/passwordChange/')
        return HttpResponse("Card owner View")


class SellerView(View):
    def get(self, request):
        try:
            Seller.objects.get(user=request.user.id)
        except Seller.DoesNotExist:
            return HttpResponse("Brak uprawnien")
        return HttpResponse("Seller View")

