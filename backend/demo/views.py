import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from .api_chat import get_recipe
from .models import Food
from django.http import JsonResponse

from .response import Response


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
            return Response.error_data(msg=f'No food for search')

        # Call async function if needed
        recipes, quantity = get_recipe(foods)
        recipes = json.loads(recipes)

        # Return response
        return Response.ok(data = {
            'success': True,
            'code': 200,
            'msg': f'Success! Found recipes. Quantity: {quantity}, Foods: {foods}, User ID: {user_id}',
            'task_id': task_id,
            'recipe': recipes
        })

    except Exception as e:
        return Response.error(msg= f'Failed to search, {e}')



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import FridgeItem, User

@csrf_exempt  # 禁用 CSRF（适用于测试，生产环境应使用 Token 认证）
def add_fridge_item(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # 解析 JSON 请求体

            # 获取字段数据
            name = data.get("name")
            tag = data.get("tag")
            expire_time = data.get("expire_time")  # 格式: "YYYY-MM-DD HH:MM:SS"
            save_time = data.get("save_time")
            pic = data.get("pic")
            uid = data.get("uid")  # 用户 ID
            
            # 验证必须字段
            if not name or not uid:
                return JsonResponse({"status": "error", "message": "Missing required fields"}, status=400)

            # 检查用户是否存在
            try:
                user = User.objects.get(id=uid)
            except User.DoesNotExist:
                return JsonResponse({"status": "error", "message": "User not found"}, status=404)

            # 创建 FridgeItem 实例
            fridge_item = FridgeItem.objects.create(
                name=name,
                tag=tag,
                expire_time=expire_time,
                save_time=save_time,
                pic=pic,
                uid=user
            )

            return JsonResponse({"status": "success", "message": "Item added", "item_id": fridge_item.id})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
