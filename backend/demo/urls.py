from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  UserViewSet, RecipeViewSet, UserRecipeLogViewSet, FridgeItemViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet,
    RecipeViewSet,
    UserRecipeLogViewSet,
    FridgeItemViewSet,
    RegisterView,
    LoginView
)


router = DefaultRouter()
router.register(r'users', UserViewSet)  # `/users/`
router.register(r'recipes', RecipeViewSet)  # `/recipes/`
router.register(r'user-recipe-log', UserRecipeLogViewSet)  # `/user-recipe-log/`
router.register(r'fridge', FridgeItemViewSet)  # `/fridge/`

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
]
