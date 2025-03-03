# from django.urls import reverse
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth import get_user_model
# from rest_framework.test import APITestCase
# from rest_framework import status

# from core.models import Recipe, UserRecipeLog, FridgeItem

# User = get_user_model()


# class UserViewSetTest(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create(
#             email="test@example.com",
#             username="testuser",
#         )
#         self.user.set_password("testpass")
#         self.user.save()
    
#     def test_list_users(self):
#         url = reverse('user-list')
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # 检查返回的用户列表中是否包含测试用户
#         self.assertTrue(any(item["email"] == self.user.email for item in response.data))
    
#     def test_create_user(self):
#         url = reverse('user-list')
#         data = {
#             "email": "newuser@example.com",
#             "username": "newuser",
#             "password": "newpass123",
#             "age": 25,
#             "height": 170,
#             "weight": 65,
#             "BMI": 22,
#             "userlike": "reading",
#             "dislike": "loud noise",
#             "allergies": "none"   # 更新字段名称
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["email"], data["email"])
    
#     def test_retrieve_user(self):
#         url = reverse('user-detail', kwargs={'pk': self.user.pk})
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["email"], self.user.email)
    
#     def test_update_user(self):
#         url = reverse('user-detail', kwargs={'pk': self.user.pk})
#         data = {
#             "email": self.user.email,  # email 一般作为标识符不变
#             "username": "updateduser",
#             "password": self.user.password,  # 密码通常不会直接更新，可在业务逻辑中处理
#             "age": 30,
#             "height": 175,
#             "weight": 70,
#             "BMI": 23,
#             "userlike": "music",
#             "dislike": "crowds",
#             "allergies": "pollen"   # 更新字段名称
#         }
#         response = self.client.put(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["username"], "updateduser")
    
#     def test_delete_user(self):
#         url = reverse('user-detail', kwargs={'pk': self.user.pk})
#         response = self.client.delete(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# class RecipeViewSetTest(APITestCase):
#     def setUp(self):
#         self.recipe = Recipe.objects.create(
#             recipe_name="Test Recipe",
#             food="Pasta",
#             recipe="Boil water and add pasta.",
#             img_url="http://example.com/image.jpg",
#             flavor_tag="Savory",
#             is_del=0
#         )
    
#     def test_list_recipes(self):
#         url = reverse('recipe-list')
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(any(item["recipe_name"] == self.recipe.recipe_name for item in response.data))
    
#     def test_create_recipe(self):
#         url = reverse('recipe-list')
#         data = {
#             "recipe_name": "New Recipe",
#             "food": "Pizza",
#             "recipe": "Prepare dough, add toppings and bake.",
#             "img_url": "http://example.com/pizza.jpg",
#             "flavor_tag": "Cheesy",
#             "is_del": 0
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["recipe_name"], data["recipe_name"])
    
#     def test_retrieve_recipe(self):
#         url = reverse('recipe-detail', kwargs={'pk': self.recipe.pk})
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["recipe_name"], self.recipe.recipe_name)
    
#     def test_update_recipe(self):
#         url = reverse('recipe-detail', kwargs={'pk': self.recipe.pk})
#         data = {
#             "recipe_name": "Updated Recipe",
#             "food": self.recipe.food,
#             "recipe": self.recipe.recipe,
#             "img_url": self.recipe.img_url,
#             "flavor_tag": self.recipe.flavor_tag,
#             "is_del": self.recipe.is_del
#         }
#         response = self.client.put(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["recipe_name"], "Updated Recipe")
    
#     def test_delete_recipe(self):
#         url = reverse('recipe-detail', kwargs={'pk': self.recipe.pk})
#         response = self.client.delete(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# class UserRecipeLogViewSetTest(APITestCase):
#     def setUp(self):
#         # 先创建有效的用户和菜谱对象
#         self.user = User.objects.create(email="loguser@example.com", username="loguser")
#         self.user.set_password("pass123")
#         self.user.save()
#         self.recipe = Recipe.objects.create(
#             recipe_name="Log Recipe",
#             food="Food",
#             recipe="Steps",
#             flavor_tag="sweet",
#             is_del=0
#         )
#         # 创建记录时传入正确的外键对象
#         self.user_recipe_log = UserRecipeLog.objects.create(
#             userid=self.user,
#             recipe_id=self.recipe,
#             op=1,
#             is_del=0
#         )
    
#     def test_list_user_recipe_logs(self):
#         url = reverse('userrecipelog-list')
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # 检查返回数据中是否包含已创建的记录
#         self.assertTrue(any(str(self.user.pk) in str(item["userid"]) for item in response.data))
    
#     def test_create_user_recipe_log(self):
#         url = reverse('userrecipelog-list')
#         # 为新记录创建另外一组用户和菜谱
#         new_user = User.objects.create(email="log2@example.com", username="loguser2")
#         new_user.set_password("pass456")
#         new_user.save()
#         new_recipe = Recipe.objects.create(
#             recipe_name="New Log Recipe",
#             food="New Food",
#             recipe="New Steps",
#             flavor_tag="spicy",
#             is_del=0
#         )
#         data = {
#             "userid": new_user.pk,
#             "recipe_id": new_recipe.pk,
#             "op": 1,
#             "is_del": 0
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["userid"], new_user.pk)
    
#     def test_retrieve_user_recipe_log(self):
#         url = reverse('userrecipelog-detail', kwargs={'pk': self.user_recipe_log.pk})
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response.data["userid"] 可能返回的是用户ID或序列化后的对象，根据序列化器而定
#         self.assertIn(str(self.user.pk), str(response.data["userid"]))
    
#     def test_update_user_recipe_log(self):
#         url = reverse('userrecipelog-detail', kwargs={'pk': self.user_recipe_log.pk})
#         data = {
#             "userid": self.user.pk,
#             "recipe_id": self.recipe.pk,
#             "op": 2,  # 修改 op 值
#             "is_del": self.user_recipe_log.is_del
#         }
#         response = self.client.put(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["op"], 2)
    
#     def test_delete_user_recipe_log(self):
#         url = reverse('userrecipelog-detail', kwargs={'pk': self.user_recipe_log.pk})
#         response = self.client.delete(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# class FridgeItemViewSetTest(APITestCase):
#     def setUp(self):
#         # 注意：假设 FridgeItemViewSet 注册时的 basename 为 "fridgeitem"
#         self.fridge_item = FridgeItem.objects.create(
#             name="Milk",
#             tag=1,
#             uid=1
#         )

#     def test_list_fridge_items(self):
#         url = reverse('fridgeitem-list')
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(any(item['name'] == self.fridge_item.name for item in response.data))

#     def test_create_fridge_item(self):
#         url = reverse('fridgeitem-list')
#         data = {
#             "name": "Eggs",
#             "tag": 2,
#             "uid": 2
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["name"], data["name"])
#         self.assertEqual(response.data["tag"], data["tag"])
#         self.assertEqual(response.data["uid"], data["uid"])

#     def test_retrieve_fridge_item(self):
#         url = reverse('fridgeitem-detail', kwargs={'pk': self.fridge_item.pk})
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["name"], self.fridge_item.name)

#     def test_update_fridge_item(self):
#         url = reverse('fridgeitem-detail', kwargs={'pk': self.fridge_item.pk})
#         data = {"name": "Updated Milk"}
#         response = self.client.patch(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["name"], "Updated Milk")

#     def test_delete_fridge_item(self):
#         url = reverse('fridgeitem-detail', kwargs={'pk': self.fridge_item.pk})
#         response = self.client.delete(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(FridgeItem.objects.filter(pk=self.fridge_item.pk).exists())


# class LoginViewTest(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create(
#             username='testuser',
#             email='test@example.com',
#             password=make_password('testpassword')
#         )
#         self.url = reverse('login')  

#     def test_login_success(self):
#         data = {
#             'email': 'test@example.com',
#             'password': 'testpassword'
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['user_id'], self.user.id)
#         self.assertEqual(response.data['email'], self.user.email)
#         self.assertEqual(response.data['username'], self.user.username)

#     def test_user_not_found(self):
#         data = {
#             'email': 'nonexistent@example.com',
#             'password': 'any_password'
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['detail'], "User not found.")

#     def test_invalid_credentials(self):
#         data = {
#             'email': 'test@example.com',
#             'password': 'wrongpassword'
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['detail'], "Invalid credentials.")


# class RegisterViewTest(APITestCase):
#     def setUp(self):
#         self.url = reverse('register')  

#     def test_register_success(self):
#         data = {
#             'username': 'newuser',
#             'email': 'newuser@example.com',
#             'password': 'newpassword123'
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(User.objects.filter(username='newuser').exists())

#     def test_register_missing_fields(self):
#         data = {
#             'username': '',
#             'email': 'newuser@example.com',
#             'password': 'newpassword123'
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
