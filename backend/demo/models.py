from django.db import models
from django.contrib.auth.models import AbstractUser
class Food(models.Model):
    Name = models.CharField(blank=True, unique=True, max_length=36)
    Production_Date = models.DateField(blank=True, null=True)
    Expire_Date = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    BMI = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    userlike = models.CharField(max_length=255, null=True, blank=True)
    dislike = models.CharField(max_length=255, null=True, blank=True)
    allergics = models.CharField(max_length=255, null=True, blank=True)
    # Set email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # You can add fields here if needed for createsuperuser

    def __str__(self):
        return self.email

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=255)
    food = models.CharField(max_length=255)
    recipe = models.TextField()
    img_url = models.CharField(max_length=255, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    flavor_tag = models.CharField(max_length=255, null=True, blank=True)
    is_del = models.IntegerField(default=0)

class UserRecipeLog(models.Model):
    userid = models.IntegerField()
    recipe_id = models.IntegerField()
    op = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_del = models.IntegerField(default=0)

class FridgeItem(models.Model):
    name = models.CharField(max_length=255)
    tag = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(null=True, blank=True)
    save_time = models.IntegerField(null=True, blank=True)
    pic = models.IntegerField(null=True, blank=True)
    is_del = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)
    uid = models.IntegerField()