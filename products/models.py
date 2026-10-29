from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from account.models import CustomUser

# Create your models here.
class Category(models.TextChoices):
    COMPUTERS = 'Computers'
    FOOD = 'Food'
    KIDS = 'Kids'
    HOME = 'Home'

class Product(models.Model):
    user        = models.ForeignKey(CustomUser,null=True, on_delete=models.SET_NULL)
    name        = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, blank=True)
    price       = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal('0.00'))
    brand       = models.CharField(max_length=200)
    category    = models.CharField(max_length=40, choices=Category.choices)
    ratings     = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.00'), blank=True, null=True, validators=[MaxValueValidator(10.00), MinValueValidator(0.00)])
    stock       = models.IntegerField(default=0)
    date        = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Review(models.Model):
    product     = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='reviews')
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.SET_NULL)
    rating      = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.00'), blank=True, null=True, validators=[MaxValueValidator(10.00), MinValueValidator(0.00)])
    comment     = models.TextField(max_length=1000, default="", blank=False)
    date        = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.comment
