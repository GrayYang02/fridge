from rest_framework import serializers
from .models import Food, User, Recipe, UserRecipeLog, FridgeItem

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'  #  自动包含所有字段

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class UserRecipeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecipeLog
        fields = '__all__'

class FridgeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeItem
        fields = '__all__'
