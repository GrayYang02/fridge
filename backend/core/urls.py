from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import UserViewSet, RecipeViewSet, UserRecipeLogViewSet, FridgeItemViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    UserViewSet,
    RecipeViewSet,
    UserRecipeLogViewSet,
    FridgeItemViewSet,
    RegisterView,
    LoginView,
    UserProfileView,
)


router = DefaultRouter()
router.register(r'users', UserViewSet)  # `/users/`
router.register(r'recipes', RecipeViewSet)  # `/recipes/`
 
router.register(r'user-recipe-log', UserRecipeLogViewSet)  # `/user-recipe-log/` 
router.register(r'fridge', FridgeItemViewSet, basename="fridge")

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api_auth/', include('rest_framework.urls')),

    # unused
    # path('get_food_list/', get_food_list, name='get_food'),
    # path('build_food_pic/', build_food_pic, name='build_food_pic'),
    # path('search_food_list/', search_food_list, name='search_food_list'),
    # path('get_recipe/', get_recipe, name='get_recipe'),

    path('profile/user-info/', UserProfileView.as_view(), name='profileinfo'),
    # path('recipe_detail/', recipe_detail_recieve, name='recipe_detail'),
]

