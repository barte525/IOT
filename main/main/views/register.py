from django.views import View
from django.shortcuts import render


class RegisterUser(View):
    def get(self, request):
        return render(request, 'register.html')