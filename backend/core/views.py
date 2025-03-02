from .models import User, Recipe, UserRecipeLog, FridgeItem
from .serializers import UserSerializer, RecipeSerializer, UserRecipeLogSerializer, FridgeItemSerializer
from rest_framework import generics, status
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist
from .models import FridgeItem, User
from .serializers import FridgeItemSerializer
from django.core.paginator import Paginator
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
)
from asgiref.sync import sync_to_async

from datetime import datetime


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

#################################################

                   #API PORT #

#################################################
def get_recipe(request):
    from .log import logger
    from dashscope import Application
    from http import HTTPStatus
    from core.settings import APP_ID, API_KEY
    from .response import Response

    try:
        # Ensure only GET requests are processed
        if request.method != "GET":
            return Response.error(msg="Invalid request method, only GET allowed")

        # Get the ingredient parameter from the request
        foods = request.GET.get('ingredient')
        user_id = request.GET.get('user_id')

        # Call the external API
        response = Application.call(
            api_key= API_KEY,
            app_id= APP_ID,
            prompt=f'My food is {foods}'
        )

        # Check response status
        if response.status_code != HTTPStatus.OK:
            msg_info = (
                f"request_id={response.request_id}, code={response.status_code}, message={response.message}.\n"
                f"See Docs: https://help.aliyun.com/zh/model-studio/developer-reference/error-code"
            )
            logger.error(msg_info)
            return Response.error(msg=msg_info)

        # Process the response

        res = response.output.text
        res_clean = extract_clean_data(res)



        if res_clean == '':
            return Response.error(msg=f"extract_clean_data failed, raw message: {res}")
        try:
            for d in res_clean['recipes']:
                Recipe.objects.create(
                    recipe_name=d['name'],
                    food=d['ingredients'],
                    recipe=d['steps'],
                    create_time=datetime.now()
                )
        except Exception as e:
            logger.error(f'failed to store info to Recipe, err_msg:{e}')
        return Response.ok(data=res_clean, msg="Successfully retrieved recipes")
    except Exception as e:
        return Response.error(msg=f"Internal Server Error: {str(e)}")

def extract_clean_data(long_string):
    from .log import logger
    try:
        # first {
        first_brace_index = long_string.find('{')

        # last }
        last_brace_index = long_string.rfind('}')

        #
        if first_brace_index != -1 and last_brace_index != -1:
            ans = long_string[first_brace_index:last_brace_index+1]
            ans = eval(ans)

            return ans
        else:
            logger.error("No related sign")

    except Exception as err:
        logger.error(err)
        logger.error('No return recipe been found')

    return ''


async def recipe_detail_recieve(request):
    from .response import Response

    temp_res = {"recipes": [
        {
            "name": "Apple and Banana Smoothie",
            "ingredients": [
                "2 medium-sized apples, peeled and chopped",
                "1 large banana, peeled",
                "1 cup of milk (dairy or non-dairy)",
                "1 tablespoon honey (optional)"
            ],
            "steps": [
                "Place the chopped apples and banana into a blender.",
                "Add the milk and honey if using.",
                "Blend all ingredients until smooth and creamy.",
                "Pour the smoothie into glasses and serve immediately."
            ]
        }
    ]
    }

    # Get the ingredient parameter from the request
    recipe_id = request.GET.get('recipe_id')
    user_id = request.GET.get('user_id')

    return Response.ok(data=temp_res, msg=f"recipe_id = {recipe_id}, user_id = {user_id}")
