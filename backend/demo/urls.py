from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_chat import get_recipe
from .views import FoodViewSet, UserViewSet, RecipeViewSet, UserRecipeLogViewSet, FridgeItemViewSet

router = DefaultRouter()
router.register(r'food', FoodViewSet)  # `/food/` 自动生成 CRUD
router.register(r'users', UserViewSet)  # `/users/`
router.register(r'recipes', RecipeViewSet)  # `/recipes/`
router.register(r'user-recipe-log', UserRecipeLogViewSet)  # `/user-recipe-log/`
router.register(r'fridge', FridgeItemViewSet)  # `/fridge/`



urlpatterns = [
    path('', include(router.urls)),  # 让 Django 处理 API 请求
    path('get_recipe/', get_recipe, name='get_recipe'),  # POST request will call this function

]
