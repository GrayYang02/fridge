from rest_framework.viewsets import ModelViewSet

from .models import User, Recipe, UserRecipeLog, FridgeItem
from .serializers import UserSerializer, RecipeSerializer, UserRecipeLogSerializer, FridgeItemSerializer, ProfileSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import action
from .pagination import UserRecipeLogPagination

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
)

from .response import Response as R


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer



class UserRecipeLogViewSet(ModelViewSet):
    queryset = UserRecipeLog.objects.all()
    serializer_class = UserRecipeLogSerializer
    permission_classes = [AllowAny]
    pagination_class = UserRecipeLogPagination
    


    @action(detail=False, methods=["post"], url_path="toggle-log")
    def toggle_user_recipe_log(self, request):
        """
        If the (userid, recipe_id, op) combination exists, toggle is_del (soft delete).
        If it does not exist, create a new record.
        """
        user_id = request.data.get("userid")
        recipe_id = request.data.get("recipe_id")
        op = request.data.get("op")

        if not user_id or not recipe_id or op is None:
            return Response({"error": "userid, recipe_id, and op are required"}, status=400)

        try:
            # Check if a record exists
            user_recipe_log = UserRecipeLog.objects.filter(
                userid=user_id, recipe_id=recipe_id, op=op
            ).first()

            if user_recipe_log:
                # Toggle is_del (soft delete/restore)
                user_recipe_log.is_del = 0 if user_recipe_log.is_del else 1
                user_recipe_log.save()
                action = "Restored" if user_recipe_log.is_del == 0 else "Deleted"
            else:
                # Create a new record if it does not exist
                user_recipe_log = UserRecipeLog.objects.create(
                    userid=user_id, recipe_id=recipe_id, op=op, is_del=0
                )
                action = "Created"

            return Response({"message": f"Record {action} successfully", "data": UserRecipeLogSerializer(user_recipe_log).data}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

  

    @action(detail=False, methods=["get"], url_path="is_collected")
    def is_recipe_collected(self, request):
        user_id = request.query_params.get("userid")
        recipe_id = request.query_params.get("recipe_id")

        if not user_id or not recipe_id:
            return Response({"error": "userid and recipe_id are required"}, status=400)

        exists = UserRecipeLog.objects.filter(
            userid=user_id, recipe_id=recipe_id, op=2, is_del=0
        ).exists()

        return Response({"is_collected": exists})

    def get_queryset(self):
        
        queryset = UserRecipeLog.objects.select_related("recipe_id").all()
        
        userid = self.request.query_params.get('userid')
        queryset = queryset.filter(userid=userid)  
        
        op = self.request.query_params.get('op')
        

        
        if op is not None:
            queryset = queryset.filter(op=int(op))

        
        queryset = queryset.filter(is_del=0)
        
        return queryset  


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
    
class UserProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        user = request.user
        # print(user)
        serializer = self.get_serializer(user)
        return R.ok(serializer.data)
        

        