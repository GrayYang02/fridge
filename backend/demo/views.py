from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Food
# Create your views here.

class Another(View):

    foods = Food.objects.all()
    output = ''
    for food in foods:
        output += f"We have {food.Name} food with ID {food.id}<br>"

    def get(self, request):
        return HttpResponse(self.output)

def first(request):
    return HttpResponse('First message from views')
