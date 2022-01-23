from main.models.card import Card
from django.views import View
from datetime import date
from django.http import JsonResponse


class CardApi(View):
    def get(self, request, cardId):
        not_exists_message = 'karta nie istnieje'
        not_active_message = 'karta nie jest aktywna'
        without_ticket_message = 'karta nie ma aktualnego biletu'
        success_message = 'karta jest aktywna i ma aktualny bilet'
        try:
            card = Card.objects.get(card_id=cardId)
        except Card.DoesNotExist:
            return JsonResponse({'aktywna':'nie', 'opis': not_exists_message})
        if not card.active:
            return JsonResponse({'aktywna':'nie', 'opis': not_active_message})
        if not card.ticket_expiration_date:
            return JsonResponse({'aktywna': 'nie', 'opis': without_ticket_message})
        if date.today() > card.ticket_expiration_date:
            return JsonResponse({'aktywna': 'nie', 'opis': without_ticket_message})
        return JsonResponse({'aktywna': 'tak', 'opis': success_message})