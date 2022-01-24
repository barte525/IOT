from main.models.card import Card
from django.views import View
from datetime import date
from django.http import JsonResponse


class CardApi(View):
    def get(self, request, cardId):
        not_exists_code = 0
        not_active_code = 1
        without_ticket_code = 2
        expired_ticket_code = 3
        success_code = 4
        try:
            card = Card.objects.get(card_id=cardId)
        except Card.DoesNotExist:
            return JsonResponse({'opis': not_exists_code})
        if not card.active:
            return JsonResponse({'opis': not_active_code})
        if not card.ticket_expiration_date:
            return JsonResponse({'opis': without_ticket_code, 'imie': card.user.user.name, 'nazwisko': card.user.user.surname})
        if date.today() > card.ticket_expiration_date:
            return JsonResponse({'opis': expired_ticket_code, 'imie': card.user.user.name, 'nazwisko': card.user.user.surname, 'termin': card.ticket_expiration_date})
        return JsonResponse({'opis': success_code, 'imie': card.user.user.name, 'nazwisko': card.user.user.surname, 'termin': card.ticket_expiration_date})