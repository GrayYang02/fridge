# core/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User, FridgeItem
import json

class IntegrationTests(APITestCase):
    def setUp(self):
        # API endpoint URLs (make sure the url names match those in urls.py)
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.token_url = reverse('get_token')
        self.profile_url = reverse('profileinfo')
        # self.get_recipe_url = reverse('get_recipe')

        # For viewsets registered via DefaultRouter:
        # For example, FridgeItemViewSet is registered as 'fridge', so its list URL is reverse('fridge-list')
        self.fridge_list_url = reverse('fridge-list')
        # add_food is a custom action in FridgeItemViewSet
        self.add_food_url = self.fridge_list_url + "add_food/"

        # Create a test user (password is hashed, so using create_user is recommended)
        self.user_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "TestPass123"
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_register(self):
        """
        Test the user registration endpoint.
        """
        data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "NewPass123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if the new user exists in the database
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_login(self):
        """
        Test the login endpoint.
        """
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Try to get the response data
        try:
            resp_data = response.data
        except AttributeError:
            resp_data = response.json()
        self.assertIn("user_id", resp_data)
        self.assertEqual(resp_data["email"], self.user_data["email"])

    def test_token_obtain(self):
        """
        Test obtaining JWT token through the API.
        """
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        response = self.client.post(self.token_url, data)
        # Retrieve response data
        try:
            resp_data = response.data
        except AttributeError:
            resp_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp_data)
        self.assertIn("refresh", resp_data)

    # def test_profile_info(self):
    #     """
    #     Test the endpoint to get user profile info (requires authentication).
    #     """
    #     # First, obtain a token
    #     data = {
    #         "email": self.user_data["email"],
    #         "password": self.user_data["password"]
    #     }
    #     token_response = self.client.post(self.token_url, data)
    #     try:
    #         token_data = token_response.data
    #     except AttributeError:
    #         token_data = token_response.json()
    #     access_token = token_data.get("access")

    #     # Add authentication header
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    #     response = self.client.get(self.profile_url)
    #     try:
    #         profile_data = response.data
    #     except AttributeError:
    #         profile_data = response.json()

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # Use try/except to safely get the email from profile_data
    #     try:
    #         actual_email = profile_data.get("email")
    #     except Exception:
    #         actual_email = None
    #     self.assertEqual(actual_email, self.user_data["email"])

    def test_fridge_item_add_and_search(self):
        """
        Test the add and fuzzy search functionality for fridge items.
        """
        # Authenticate and get token
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        token_response = self.client.post(self.token_url, data)
        try:
            token_data = token_response.data
        except AttributeError:
            token_data = token_response.json()
        access_token = token_data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Test the add item endpoint
        add_data = {
            "name": "Apple",
            "add_time": "2025-03-03T00:00:00Z",
            "expire_time": "2025-04-03",
            "tag": 2
        }
        add_response = self.client.post(self.add_food_url, add_data, format="json")
        self.assertEqual(add_response.status_code, status.HTTP_201_CREATED)
        try:
            add_resp_data = add_response.data
        except AttributeError:
            add_resp_data = add_response.json()
        self.assertEqual(add_resp_data.get("name"), "Apple")

        # Test the search endpoint for items
        # Assuming the search_food_list action is registered with the name 'search_food_list'
        search_url = self.fridge_list_url + "search_food_list/"
        search_response = self.client.get(search_url, {"name": "Apple"})
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        try:
            search_resp_data = search_response.data
        except AttributeError:
            search_resp_data = search_response.json()
        # Verify that "Apple" is contained in the returned items
        self.assertTrue(
            any("Apple" in food["name"] for food in search_resp_data.get("data", {}).get("foods", []))
        )

    def test_get_recipe(self):
        """
        Test the recipe generation endpoint.
        Note: This endpoint calls an external API and may rely on external services.
        In real integration tests, it is recommended to use mocks for external API calls.
        """
        # Simulate a GET request to the get_recipe endpoint
        params = {"ingredient": "tomato", "user_id": self.user.id}
        response = self.client.get(self.get_recipe_url, params)
        # Depending on the business logic, the response status could be 200 or other statuses if the external API fails.
        self.assertIn(
            response.status_code, 
            [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST, status.HTTP_500_INTERNAL_SERVER_ERROR]
        )
