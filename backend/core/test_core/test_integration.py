# tests/test_integration.py

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class FullIntegrationTest(APITestCase):
    def test_full_flow(self):
        register_url = reverse('core:register')
        register_data = {
            "username": "integrationuser",
            "email": "integrationuser@example.com",
            "password": "integrationpass"
        }
        response = self.client.post(register_url, register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        login_url = reverse('core:login')
        login_data = {
            "email": "integrationuser@example.com",
            "password": "integrationpass"
        }
        response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data.get("user_id")
        user = User.objects.get(id=user_id)
        
        self.client.force_authenticate(user=user)
        
        add_food_url = reverse('core:fridge-add-food')
        add_food_data = {
            "name": "Test Milk",
            "tag": 1,
            "add_time": "2025-03-05T12:00:00Z",   
            "expire_time": "2099-12-31"           
        }
        response = self.client.post(add_food_url, add_food_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        food_list_url = reverse('core:fridge-food-list')
        response = self.client.get(food_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        foods = response.data.get("foods", [])
        self.assertGreaterEqual(len(foods), 1)
        
        recipe_url = reverse('core:recipe-list')
        recipe_data = {
            "recipe_name": "Integration Recipe",
            "food": "Test Food",
            "recipe": "Mix ingredients well.",
            "img_url": "http://example.com/image.jpg",
            "flavor_tag": "Sweet",
            "is_del": 0,
            "uid": user.id
        }
        response = self.client.post(recipe_url, recipe_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe_id = response.data.get("id")
        
        toggle_log_url = reverse('core:userrecipelog-toggle-user-recipe-log')
        toggle_data = {
            "userid": user.id,
            "recipe_id": recipe_id,
            "op": 1
        }
        response = self.client.post(toggle_log_url, toggle_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        profile_url = reverse('core:profileinfo')
        response = self.client.get(profile_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data.get("username"), "integrationuser")
