from django.db import models

class Food(models.Model):
    Name = models.CharField(blank=True, unique=True, max_length=36)
    Production_Date = models.DateField(blank=True, null=True)
    Expire_Date = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.name
