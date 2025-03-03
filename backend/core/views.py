from .models import User, Recipe, UserRecipeLog, FridgeItem, PicUrls
from .serializers import UserSerializer, RecipeSerializer, UserRecipeLogSerializer, FridgeItemSerializer, ProfileSerializer
from rest_framework import generics, status
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from rest_framework.views import APIView
from rest_framework.decorators import action
from .pagination import UserRecipeLogPagination

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
from asgiref.sync import sync_to_async

from datetime import datetime
FOOD_TAGS = {
    1: {"name": "meat", "icon": "/icons/meat.png"},
    2: {"name": "vegetable", "icon": "/icons/vegetable.png"},
    3: {"name": "dairy", "icon": "/icons/dairy.png"}
}

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
    permission_classes = [IsAuthenticated]  
    def get_queryset(self):
        """确保用户只能看到自己的食物"""
        return FridgeItem.objects.filter(user=self.request.user)


    @action(detail=False, methods=['post'])
    def add_food(self, request):
        print(f"Authenticated user: {request.user}")  
        print(f"Authenticated user: {request.user.id}") 

        if request.user.is_anonymous:
            return Response({"error": "Unauthorized - Invalid Token"}, status=401)
        food_name = request.data.get('name')
        user_id = request.user.id
        add_time = request.data.get('add_time')
        expire_time = request.data.get('expire_time')
        tag = request.data.get('tag')

        # Check if user exists
        # user = get_object_or_404(User, id=user_id)

        # Create FridgeItem
        fridge_item = FridgeItem.objects.create(
            name=food_name,
            uid=user_id,
            create_time=add_time,
            expire_time=expire_time,
            tag=tag
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

        """获取食物列表，支持分页、排序、按用户 ID 过滤，并根据 keyword 进行模糊查询"""
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        sort_by = request.query_params.get('sort_by', 'create_time_desc')
        keyword = request.query_params.get('keyword', '').strip()
        tag = request.query_params.get('tag', None)

        queryset = FridgeItem.objects.filter(uid=request.user.id, is_del=0)

        # 按 tag 过滤
        if tag is not None:
            try:
                tag = int(tag)
                if tag in FOOD_TAGS:
                    queryset = queryset.filter(tag=tag)
                else:
                    return Response({"error": "Invalid tag value"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "Tag must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 按名称模糊匹配
        if keyword:
            queryset = queryset.filter(Q(name__icontains=keyword))
        
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

        food_data = FridgeItemSerializer(foods, many=True).data
        for food in food_data:
            food["icon"] = FOOD_TAGS.get(food["tag"], {}).get("icon", "")

        return Response({
            "total": paginator.count,
            "page": page,
            "page_size": page_size,
            "foods": food_data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def food_tags(self, request):
        """获取所有食品标签及其 icon"""
        return Response(FOOD_TAGS, status=status.HTTP_200_OK)

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
    


    def get_queryset(self):
        """确保用户只能看到自己的食物"""
        return FridgeItem.objects.filter(user=self.request.user)


    # @action(detail=False, methods=['post'])
    # def add_food(self, request):
    #     food_name = request.data.get('name')
    #     user_id = request.data.get('user_id')
    #     add_time = request.data.get('add_time')
    #     expire_time = request.data.get('expire_time')

    #     # Check if user exists
    #     # user = get_object_or_404(User, id=user_id)

    #     # Create FridgeItem
    #     fridge_item = FridgeItem.objects.create(
    #         name=food_name,
    #         uid=user_id,
    #         create_time=add_time,
    #         expire_time=expire_time,
    #         tag=1
    #     )
    #     return Response({
    #         'id': fridge_item.id,
    #         'name': fridge_item.name,
    #         'pic': fridge_item.pic,
    #         'create_time': fridge_item.create_time,
    #         'expire_time': fridge_item.expire_time
    #     }, status=status.HTTP_201_CREATED)
    
    # @action(detail=False, methods=['get'])
    # def food_list(self, request):
    #     """获取食物列表，支持分页和排序"""
    #     page = int(request.query_params.get('page', 1))
    #     page_size = int(request.query_params.get('page_size', 10))
    #     sort_by = request.query_params.get('sort_by', 'create_time_desc')

    #     # queryset = FridgeItem.objects.filter(user=request.user)
    #     queryset = FridgeItem.objects.filter()
    #     # 排序逻辑
    #     if sort_by == 'tag':
    #         queryset = queryset.order_by('tag')
    #     elif sort_by == 'create_time':
    #         queryset = queryset.order_by('create_time')
    #     elif sort_by == 'create_time_desc':
    #         queryset = queryset.order_by('-create_time')
    #     else:
    #         return Response({"error": "Invalid sort_by parameter"}, status=status.HTTP_400_BAD_REQUEST)

    #     paginator = Paginator(queryset, page_size)
    #     foods = paginator.get_page(page)

    #     return Response({
    #         "total": paginator.count,
    #         "page": page,
    #         "page_size": page_size,
    #         "foods": FridgeItemSerializer(foods, many=True).data
    #     }, status=status.HTTP_200_OK)

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
    
class UserProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        user = request.user
        # print(user)
        serializer = self.get_serializer(user)
        return R.ok(serializer.data)
        


    #         return Response({
    #             "id": user.id,
    #             "username": user.username,
    #             "email": user.email,
    #         })


def get_food_list(request):
    from .response import Response
    from .log import logger
    try:
        uid = request.GET.get('uid')
        if uid == '':
            return Response.error(msg=f'[user_id] not valid: {uid}')
        uid = int(uid)
        queryset = FridgeItem.objects.filter(uid=uid).order_by('create_time')

        if not queryset:
            return Response.error(msg='Failed to fetch items')
        foods = []
        tags = ['sweet', 'spicy', 'salty', 'creamy', 'savory']
        for item in queryset:
            pic = PicUrls.objects.filter(name=item.name).first()
            foods.append({"name":item.name, "pic":pic.url})
        return Response.ok(data={"foods": foods, "tags": tags }, msg="Received all the foods")

    except Exception as err:
        # Log the error for debugging
        print(f"Error: {err}")
        # Return a serializable error message
        return Response.error(msg=str(err))



def build_food_pic(request):
    from .response import Response

    # default_data = {'beef':'https://images.unsplash.com/photo-1602473812169-ede177b00aea?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    #                  }
    # for name, pic_url in default_data.items():
    #     PicUrls.objects.update_or_create(
    #         name=name,
    #         url=pic_url
    #     )
    # pic = PicUrls.objects.filter(name='beef').first()
    # print(pic.url)
    return Response.ok(msg="Received all the foods")


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
        user_id = int(request.GET.get('user_id'))

        # Call the external API
        response = Application.call(
            api_key= API_KEY,
            app_id= APP_ID,
            prompt=f'My food is {foods}, output in [dict] format!'
        )

        # Check response status
        if response.status_code != HTTPStatus.OK:
            msg_info = (
                f"request_id={response.request_id}, code={response.status_code}, message={response.message}.\n"
                f"See Docs: https://help.aliyun.com/zh/model-studio/developer-reference/error-code"
            )
            logger.error(msg_info)
            return Response.error(msg=msg_info)


        res = response.output.text
        res_clean = extract_clean_data(res)

        if res_clean == '':
            return Response.error(msg=f"extract_clean_data failed, raw message: {res}")
        try:
            for d in res_clean['recipes']:
                Recipe.objects.create(
                    recipe_name=d['name'],
                    food=d['ingredients'],
                    flavor_tag=d['flavor_tag'],
                    recipe=d['steps'],
                    uid=user_id,
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

