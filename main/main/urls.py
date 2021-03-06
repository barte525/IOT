"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from main.views.manage_profiles import ManageProfiles, CardOwnerView, SellerView
from main.views.main import Main, OfferView
from main.views.register import RegisterUser, RegisterUserResponse
from main.views.seller_buy import SellerBuyTicket, SellerBuyTicketSave
from main.views.card_owner import CardOwnerStatusView, CardOwnerBuyTicketView, CardOwnerConfirmBuyTicketView
from main.views.api import CardApi

urlpatterns = [
    path('', Main.as_view()),
    path('admin/', admin.site.urls),
    path('zaloguj/', auth_views.LoginView.as_view(template_name="login.html")),
    path('wyloguj/', auth_views.LogoutView.as_view(template_name="logout.html")),
    path('oferta/', OfferView.as_view()),
    path('profil/', ManageProfiles.as_view()),
    path('profil/uzytkownikKarty/', CardOwnerView.as_view()),
    path('profil/sprzedawca/', SellerView.as_view()),
    path('profil/zmianaHasla/', auth_views.PasswordChangeView.as_view(success_url='/profil/',
                                                                      template_name='password_change.html')),
    path('profil/sprzedawca/', include([
        path('rejestracja/', RegisterUser.as_view()),
        path('rejestracja/', include([
            path('zatwierdzenie', RegisterUserResponse.as_view()),
        ])),
        path('zakupBiletu/', SellerBuyTicket.as_view()),
        path('zakupBiletu/', include([
            path('<str:cardId>/<uuid:ticketId>', SellerBuyTicketSave.as_view()),
            path('zatwierdzenie', SellerBuyTicketSave.as_view()),
        ])),
    ])),

    # path('profil/sprzedawca/rejestracja/', RegisterUser.as_view()),
    # path('profil/sprzedawca/zakupBiletu', SellerBuyTicket.as_view()),
    # path('profil/sprzedawca/zakupBiletu/<str:cardId>/<uuid:ticketId>', SellerBuyTicketSave.as_view()),
    # path('profil/sprzedawca/zakupBiletu/sukces', SellerBuyTicketSave.as_view()),

    path('profil/uzytkownikKarty/', include([
        path('statusKarty', CardOwnerStatusView.as_view()),
        path('zakupBiletu/', include([
            path('<uuid:ticket_id>', CardOwnerBuyTicketView.as_view()),
            path('zatwierdzenie', CardOwnerConfirmBuyTicketView.as_view()),
            path('zatwierdzenie/<uuid:trans_id>', CardOwnerConfirmBuyTicketView.as_view()),
        ])),
    ])),

    path('api/czy_aktywna/<str:cardId>', CardApi.as_view()),

]
