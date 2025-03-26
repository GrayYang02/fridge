from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Recipe, UserRecipeLog, FridgeItem

User = get_user_model()

class UserViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com",
            username="testuser",
        )
        self.user.set_password("testpass")
        self.user.save()
    
    def test_list_users(self):
        url = reverse('core:user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user(self):
        url = reverse('core:user-list')
        data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpass123",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_retrieve_user(self):
        url = reverse('core:user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        url = reverse('core:user-detail', kwargs={'pk': self.user.pk})
        data = {"username": "updateduser"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_user(self):
        url = reverse('core:user-detail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RecipeViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="recipeuser@example.com", username="recipeuser")
        self.recipe = Recipe.objects.create(
            recipe_name="Test Recipe",
            food="Pasta",
            recipe="Boil water and add pasta.",
            img_url="http://example.com/image.jpg",
            flavor_tag="Savory",
            is_del=0,
            uid=self.user.id  
        )

    def test_list_recipes(self):
        url = reverse('core:recipe-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserRecipeLogViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="loguser@example.com", username="loguser")
        self.recipe = Recipe.objects.create(
            recipe_name="Log Recipe",
            food="Food",
            recipe="Steps",
            flavor_tag="sweet",
            is_del=0,
            uid=self.user.id  
        )
        self.user_recipe_log = UserRecipeLog.objects.create(
            userid=self.user,
            recipe_id=self.recipe,
            op=1,
            is_del=0
        )

    def test_list_user_recipe_logs(self):
        url = reverse('core:userrecipelog-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # def test_create_user_recipe_log(self):
    #     url = reverse('core:userrecipelog-list')
    #     data = {
    #         "userid": self.user.pk,
    #         "recipe_id": self.recipe.pk,
    #         "op": 1,
    #         "is_del": 0
    #     }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_toggle_user_recipe_log(self):
        url = reverse('core:userrecipelog-toggle-user-recipe-log')  
        data = {
            "userid": self.user.pk,
            "recipe_id": self.recipe.pk,
            "op": 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import FridgeItem

User = get_user_model()

class FridgeItemViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="fridgeuser", 
            email="fridgeuser@example.com", 
            password="testpass"
        )
        self.client.force_authenticate(user=self.user)
        self.fridge_item = FridgeItem.objects.create(
            name="Milk",
            tag=1,
            uid=self.user.id 
        )

    # def test_list_fridge_items(self):
    #     url = reverse('core:fridge-list')
    #     response = self.client.get(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_fridge_item(self):
        url = reverse('core:fridge-list')
        data = {
            "name": "Eggs",
            "tag": 2,
            "uid": self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password=make_password('testpassword')
        )
        self.url = reverse('core:login')

    def test_login_success(self):
        data = {"email": "test@example.com", "password": "testpassword"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_credentials(self):
        data = {"email": "test@example.com", "password": "wrongpassword"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RegisterViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('core:register')

    def test_register_success(self):
        data = {"username": "newuser", "email": "newuser@example.com", "password": "newpassword123"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
