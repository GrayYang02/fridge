from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  UserViewSet, RecipeViewSet, UserRecipeLogViewSet, FridgeItemViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)  # `/users/`
router.register(r'recipes', RecipeViewSet)  # `/recipes/`
router.register(r'user-recipe-log', UserRecipeLogViewSet)  # `/user-recipe-log/`
router.register(r'fridge', FridgeItemViewSet)  # `/fridge/`

urlpatterns = [
    path('', include(router.urls)),  # 让 Django 处理 API 请求
]
