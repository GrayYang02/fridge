from rest_framework.viewsets import ModelViewSet

from .models import User, Recipe, UserRecipeLog, FridgeItem
from .serializers import UserSerializer, RecipeSerializer, UserRecipeLogSerializer, FridgeItemSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist
from .models import FridgeItem, User
from .serializers import FridgeItemSerializer
from django.core.paginator import Paginator
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
    permission_classes = [IsAuthenticated]  
    def get_queryset(self):
        """确保用户只能看到自己的食物"""
        return FridgeItem.objects.filter(user=self.request.user)


    @action(detail=False, methods=['post'])
    def add_food(self, request):
        food_name = request.data.get('name')
        user_id = request.data.get('user_id')
        add_time = request.data.get('add_time')
        expire_time = request.data.get('expire_time')

        # Check if user exists
        # user = get_object_or_404(User, id=user_id)

        # Create FridgeItem
        fridge_item = FridgeItem.objects.create(
            name=food_name,
            uid=user_id,
            create_time=add_time,
            expire_time=expire_time,
            tag=1
        )
        return Response({
            'id': fridge_item.id,
            'name': fridge_item.name,
            'pic': fridge_item.pic,
            'create_time': fridge_item.create_time,
            'expire_time': fridge_item.expire_time
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def food_list(self, request):
        print(f"Authenticated user: {request.user}")  
        print(f"Authenticated user: {request.user.id}") 

        if request.user.is_anonymous:
            return Response({"error": "Unauthorized - Invalid Token"}, status=401)

        """获取食物列表，支持分页和排序"""
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        sort_by = request.query_params.get('sort_by', 'create_time_desc')

        # queryset = FridgeItem.objects.filter(user=request.user)
        queryset = FridgeItem.objects.filter()
        # 排序逻辑
        if sort_by == 'tag':
            queryset = queryset.order_by('tag')
        elif sort_by == 'create_time':
            queryset = queryset.order_by('create_time')
        elif sort_by == 'create_time_desc':
            queryset = queryset.order_by('-create_time')
        else:
            return Response({"error": "Invalid sort_by parameter"}, status=status.HTTP_400_BAD_REQUEST)

        paginator = Paginator(queryset, page_size)
        foods = paginator.get_page(page)

        return Response({
            "total": paginator.count,
            "page": page,
            "page_size": page_size,
            "foods": FridgeItemSerializer(foods, many=True).data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def delete_food(self, request):
        """删除食物"""
        food_id = request.data.get('food_id')
        
        try:
            food = FridgeItem.objects.get(id=food_id)
        except ObjectDoesNotExist:
            return Response({"error": "Food not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

        food.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)
    

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
    
    # class UserProfileView(APIView):
    #     permission_classes = [IsAuthenticated]  

    #     def get(self, request):
    #         user = request.user

    #         return Response({
    #             "id": user.id,
    #             "username": user.username,
    #             "email": user.email,
    #         })