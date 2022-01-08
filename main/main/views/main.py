from django.views import View
from django.shortcuts import render, redirect


class Main(View):
    def get(self, request):
        return render(request, 'main_page.html')