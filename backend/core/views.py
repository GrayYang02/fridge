from rest_framework.viewsets import ModelViewSet

from .models import User, Recipe, UserRecipeLog, FridgeItem
from .serializers import UserSerializer, RecipeSerializer, UserRecipeLogSerializer, FridgeItemSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
)


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
    

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(password, user.password):
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "user_id": user.id,
            "email": user.email,
            "username": user.username
        }, status=status.HTTP_200_OK)
    
    class UserProfileView(APIView):
        permission_classes = [IsAuthenticated]  

        def get(self, request):
            user = request.user
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }, status=status.HTTP_200_OK)