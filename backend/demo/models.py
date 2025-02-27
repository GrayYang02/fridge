from django.db import models
import datetime

class Food(models.Model):
    Name = models.CharField(blank=True, unique=True, max_length=36)
    Production_Date = models.DateField(default=datetime.date.today)
    Expire_Date = models.DateField(default=lambda: datetime.date.today() + datetime.timedelta(days=30))
    def __str__(self):
        return self.name

class User(models.Model):
    email = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    BMI = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(default=datetime.date.today)
    update_time = models.DateTimeField(default=datetime.date.today)
    userlike = models.CharField(max_length=255, null=True, blank=True)
    dislike = models.CharField(max_length=255, null=True, blank=True)
    allergics = models.CharField(max_length=255, null=True, blank=True)

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=255)
    food = models.CharField(max_length=255)
    recipe = models.TextField()
    img_url = models.CharField(max_length=255, null=True, blank=True)
    create_time = models.DateTimeField(default=datetime.date.today)
    update_time = models.DateTimeField(default=datetime.date.today)
    flavor_tag = models.CharField(max_length=255, null=True, blank=True)
    is_del = models.IntegerField(default=0)

class UserRecipeLog(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    op = models.IntegerField()
    create_time = models.DateTimeField(default=datetime.date.today)
    update_time = models.DateTimeField(default=datetime.date.today)
    is_del = models.IntegerField(default=0)

class FridgeItem(models.Model):
    name = models.CharField(max_length=255)
    tag = models.IntegerField()
    create_time = models.DateTimeField(default=datetime.date.today)
    expire_time = models.DateTimeField(default=lambda: datetime.date.today() + datetime.timedelta(days=30)) # 默认30天
    save_time = models.IntegerField(default=30) # default 90 days
    pic = models.IntegerField(null=True, blank=True)
    is_del = models.IntegerField(default=0)
    update_time = models.DateTimeField(default=datetime.date.today)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
