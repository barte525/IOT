from django.views import View
from django.shortcuts import render


class Main(View):
    def get(self, request):
        return render(request, 'main_page.html')