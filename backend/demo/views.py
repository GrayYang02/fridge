from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import  User, Recipe, UserRecipeLog, FridgeItem
from .serializers import UserSerializer, RecipeSerializer, UserRecipeLogSerializer, FridgeItemSerializer



class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class UserRecipeLogViewSet(ModelViewSet):
    queryset = UserRecipeLog.objects.all()
    serializer_class = UserRecipeLogSerializer


class FridgeItemViewSet(ModelViewSet):
    queryset = FridgeItem.objects.all()
    serializer_class = FridgeItemSerializer
