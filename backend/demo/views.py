import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from .api_chat import get_recipe
from .models import Food
from django.http import JsonResponse



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

async def recipe_quest(request):
    try:
        # Extract query parameters correctly
        foods = request.GET.get('foods', '')
        user_id = request.GET.get('user_id', '')
        task_id = request.GET.get('task_id', '')
        if foods == '':
            return JsonResponse({'success': False, 'code': 400, 'msg': f'No food for search'})

        # Call async function if needed
        recipes, quantity = get_recipe(foods)
        recipes = json.loads(recipes)

        # Return response
        return JsonResponse({
            'success': True,
            'code': 200,
            'msg': f'Success! Found recipes. Quantity: {quantity}, Foods: {foods}, User ID: {user_id}',
            'task_id': task_id,
            'recipe': recipes
        }, json_dumps_params={'ensure_ascii': False})

    except Exception as e:
        return JsonResponse({'success': False, 'code': 400, 'msg': f'Failed to search, {e}'})