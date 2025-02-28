from rest_framework import serializers
from .models import  User, Recipe, UserRecipeLog, FridgeItem
from django.contrib.auth.hashers import make_password, check_password

class RegisterSerializer(serializers.ModelSerializer):
    """
    专门处理注册逻辑，哈希用户密码
    """
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password is not None:
            user.password = make_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    专门处理登录逻辑
    """
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

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