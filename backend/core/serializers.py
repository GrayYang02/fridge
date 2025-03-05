from rest_framework import serializers
from .models import  User, Recipe, UserRecipeLog, FridgeItem
from django.contrib.auth.hashers import make_password, check_password

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False)
    email = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)
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

    email = serializers.EmailField()

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
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()  
    )
    recipe_details = serializers.SerializerMethodField() 
    class Meta:
        model = UserRecipeLog
        fields = ["id","userid", "recipe_id", "recipe_details", "op", "create_time", "is_del"]
    def get_recipe_details(self, obj):
        if obj.recipe_id:
            return RecipeSerializer(obj.recipe_id).data 
        return None

class FridgeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeItem
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'age', 'height', 'weight', 'BMI', 'userlike', 'dislike', 'allergies']
        extra_kwargs = {
            'email': {'write_only': True}
        }
    


    # def update(self, instance, validated_data):
        
    #     password = validated_data.pop('password', None) 
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value) 

    #     if password:  
    #         instance.set_password(password) 

    #     instance.save()
    #     return instance