import json

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
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404

from rest_framework.parsers import MultiPartParser, FormParser
FOOD_TAGS = {
    1: {"name": "meat", "icon": "/icons/meat.png"},
    2: {"name": "vegetable", "icon": "/icons/vegetable.png"},
    3: {"name": "dairy", "icon": "/icons/dairy.png"},
    4: {"name": "staple", "icon": "/icons/staple.png"},
    5: {"name": "fruit", "icon": "/icons/fruit.png"},
    6: {"name": "egg", "icon": "/icons/egg.png"}

}

from .response import Response as R



class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    @action(detail=False, methods=["get"], url_path="daily_recommand")
    def user_daily_recommandation(self, request):
        from core.settings import SUGGEST_APP_ID, API_KEY
        from .response import Response
        from .log import logger
        from dashscope import Application
        from http import HTTPStatus
        try:
            # Ensure only GET requests are processed
            if request.method != "GET":
                return Response.error(msg="Invalid request method, only GET allowed")

            uid = int(request.query_params.get("userid"))
            user_profile = User.objects.filter(id=uid).first()
            # age = user_profile.age
            BMI = user_profile.BMI
            userlike = user_profile.userlike
            allergies = user_profile.allergies

            response = Application.call(

                api_key=API_KEY,
                app_id=SUGGEST_APP_ID,
                prompt=f'Hi! I need a 1-day meal plan.Here’s my profile:Allergies:{allergies} '
                       f'Taste Preferences:{userlike}'
                       f'BMI: {BMI}'
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

            parsed_data = json.loads(res)

            if res == '':
                return Response.error(msg=f"extract_clean_data failed, raw message: {res}")

        except Exception as e:
            return Response.error(msg=e)

        return Response.ok(data=parsed_data, msg=f"Success in user_id = {uid}")

    parser_classes = (MultiPartParser, FormParser)


    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Use partial=True to allow updating only some fields
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                "code": 200,
                "msg": "User updated successfully!",
                "data": serializer.data
            })
        return Response({
            "code": 400,
            "msg": "Validation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


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
    
        user_id = request.data.get("userid")
        recipe_id = request.data.get("recipe_id")
        op = request.data.get("op")

        if not user_id or not recipe_id or op is None:
            return Response({"error": "userid, recipe_id, and op are required"}, status=400)

        try:
            user = get_object_or_404(User, id=user_id) 
            recipe = get_object_or_404(Recipe, id=recipe_id)

            # Check if a record exists
            user_recipe_log = UserRecipeLog.objects.filter(
                userid=user, recipe_id=recipe, op=op
            ).first()
            print(UserRecipeLogSerializer(user_recipe_log).data)
            
            
            if user_recipe_log:
                if op in [2]:  
                    user_recipe_log.is_del = 0 if user_recipe_log.is_del else 1
                    user_recipe_log.save()
                    action = "Restored" if user_recipe_log.is_del == 0 else "Deleted"
                else:
                    action = "No action needed" 
            else:
                # Create a new record if it does not exist
                user_recipe_log = UserRecipeLog.objects.create(
                    userid=user, recipe_id=recipe, op=op, is_del=0
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
        return FridgeItem.objects.filter(uid=self.request.user.id)

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
    def search_food_list(self, request):
        from .response import Response
        user = request.user
        uid = user.id
        name = request.GET.get('name')

        if name:
            fridge_items = FridgeItem.objects.filter(uid=uid, name__icontains=name).order_by('expire_time')
        else:
            fridge_items = FridgeItem.objects.filter(uid=uid).order_by('expire_time')

        foods = []
        for item in fridge_items:
            # pic = PicUrls.objects.filter(name=item.name).first()
            tag_icon = FOOD_TAGS.get(item.tag, {}).get("icon", "") 
            foods.append({
                "name": item.name,
                "pic": tag_icon,
                "tag_icon": tag_icon,
                "expire_time":item.expire_time,
            })
        
        flatags = ['sweet', 'spicy', 'salty', 'creamy', 'savory']

        return Response.ok(data={"foods": foods, "tags": flatags}, msg="Received all the foods")


    @action(detail=False, methods=['get'])
    def food_list(self, request):
        print(f"Authenticated user: {request.user}")  
        print(f"Authenticated user: {request.user.id}") 

        if request.user.is_anonymous:
            return Response({"error": "Unauthorized - Invalid Token"}, status=401)

        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        sort_by = request.query_params.get('sort_by', 'create_time_desc')
        keyword = request.query_params.get('keyword', '').strip()
        tag = request.query_params.get('tag', None)
        is_expire = request.query_params.get('is_expire', None)

        queryset = FridgeItem.objects.filter(uid=request.user.id, is_del=0)

        if tag is not None:
            try:
                tag = int(tag)
                if tag in FOOD_TAGS:
                    queryset = queryset.filter(tag=tag)
                else:
                    return Response({"error": "Invalid tag value"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "Tag must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        if keyword:
            queryset = queryset.filter(name__icontains=keyword)
        now = timezone.now()
        expire_threshold = now + timedelta(days=1)
        if is_expire is not None:
            
            queryset = queryset.filter(expire_time__lte=expire_threshold).order_by('expire_time')
        else:
            queryset = queryset.filter(expire_time__gt=expire_threshold)


        
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
        return Response(FOOD_TAGS, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def delete_food(self, request):
        food_id = request.data.get('food_id')
        
        try:
            food = FridgeItem.objects.get(id=food_id)
        except ObjectDoesNotExist:
            return Response({"error": "Food not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

        food.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)
    


    # def get_queryset(self):
    #     return FridgeItem.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def get_recipe(self,request):
        from .log import logger
        from dashscope import Application
        from http import HTTPStatus
        from core.settings import RECIPE_APP_ID, API_KEY
        from .response import Response
        from datetime import datetime
        from .models import Recipe
        print(f"Authenticated user: {request.user}")  
        print(f"Authenticated user: {request.user.id}") 

        if request.user.is_anonymous:
            return Response({"error": "Unauthorized - Invalid Token"}, status=401)
        try:
            if request.method != "GET":
                return Response.error(msg="Invalid request method, only GET allowed")

            foods = request.GET.get('ingredient')
            user_id = request.user.id
            if foods == '':
                return Response.error(msg="cannot generate with no food")
  
            response = Application.call(

                api_key= API_KEY,
                app_id= RECIPE_APP_ID,
                prompt=f'My food is {foods},generate English recipe! remember to output in [dict] format!'
            )

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
            
            recipes_with_ids = []
            try:
                for d in res_clean['recipes']:
                    recipe = Recipe.objects.create(
                        recipe_name=d['name'],
                        food=d['ingredients'],
                        calories=d['calories'],
                        flavor_tag=d['flavor_tag'],
                        recipe=d['steps'],
                        uid=user_id,
                        create_time=datetime.now()
                    )
                    d['id'] = recipe.id 
                    recipes_with_ids.append(d)
            except Exception as e:
                logger.error(f'failed to store info to Recipe, err_msg:{e}')
            
            return Response.ok(data={'recipes': recipes_with_ids}, msg="Successfully retrieved recipes")
        except Exception as e:
            return Response.error(msg=f"Internal Server Error: {str(e)}")

    @action(detail=False, methods=['delete'])
    def delete_food(self, request):
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
    print("Signup error:", serializer_class.errors)

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
    
# class UserProfileView(generics.GenericAPIView):
#     serializer_class = ProfileSerializer
#     # permission_classes = [IsAuthenticated]  

#     def get(self, request):
#         user = request.user
#         # print(user)
#         serializer = self.get_serializer(user)
#         return R.ok(serializer.data)

class UserProfileView(APIView):
    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        user = request.user
        print(user)
        serializer = ProfileSerializer(user)
        return R.ok(serializer.data)

    def patch(self, request, format=None):
        user = request.user
        print(request.data)
        serializer = ProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return R.ok(serializer.data)
        return R.error(serializer.errors)
        


    #         return Response({
    #             "id": user.id,
    #             "username": user.username,
    #             "email": user.email,
    #         })


def get_food_list(request):
    from .response import Response

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
        print(f"Error: {err}")
        return Response.error(msg=str(err))



def shopping_list(request):
    from .response import Response
    try:
        uid = int(request.GET.get('userid'))
        recipe_id = request.GET.get('recipe_id')
        print(uid, recipe_id)

        fridge_items = FridgeItem.objects.filter(uid=uid).first()
        fridge_foods = [fridge_items.name] if fridge_items else []
        recipe = Recipe.objects.filter(uid=uid, id=recipe_id).first()
        if not recipe:
            return Response.error(msg="Recipe not found")

        recipe_food = eval(recipe.food)
        # print(recipe_food, fridge_foods)
        missing_items = list(set(recipe_food) - set(fridge_foods))

        # print(missing_items)
        # return missing_items
        return Response.ok(data=missing_items,
                           msg=f"Success find purchase list recipe_id = {recipe_id}, user_id = {uid}")

    except Exception as e:
        return Response.error(msg=f"generate shopping_list Error: {str(e)}")


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
            ans = ans.replace('\n', '')
            ans.strip()
            ans = eval(ans)

            return ans
        else:
            logger.error("No related sign")

    except Exception as err:
        logger.error(err)
        logger.error('No return recipe been found')

    return ''


def recipe_detail_recieve(request):
    from django.forms.models import model_to_dict
    from .response import Response  
    uid = request.GET.get('user_id')  
    id = request.GET.get('id')
    if not uid or not id:
        return Response.error(msg="Missing user_id or id")
    uid = int(uid)
    id = int(id)
    try:
        recipe = Recipe.objects.filter(uid=uid, id=id).first()
        if not recipe:
            return Response.error(msg="Recipe not found")

        recipe_data = model_to_dict(recipe)

    except Exception as e:
        return Response.error(msg=f"Error retrieving recipe: {str(e)}")

    return Response.ok(data=recipe_data, msg=f"Success in recipe_id = {id}, user_id = {uid}")



