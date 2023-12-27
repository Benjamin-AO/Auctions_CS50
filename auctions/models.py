from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    Category_label = models.CharField(max_length=64)

    def __str__(self):
        return self.Category_label


class Listings(models.Model):
    title = models.CharField(max_length=64)
    item_description = models.CharField(max_length=500)
    asking_price = models.FloatField()
    imageUrl = models.CharField(max_length=2000)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    available = models.BooleanField(default=True)
    item_category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="category")

    def __str__(self):
        return f"{self.id}:{self.title}"

class Bid(models.Model):
    pass


class Comments(models.Model):
    pass