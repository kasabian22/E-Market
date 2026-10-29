from django.db import models
from operator import mod
from products.models import Product
from account.models import CustomUser
# Order has three stages: Proccessing, Shipping, delivered.

class OrderStatus(models.TextChoices):
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'

class PaymentStatus(models.TextChoices):
    PAID = 'Paid'
    UNPAID = 'Unpaid'
    
class PaymentMethod(models.TextChoices):
    COD = 'COD' # cash on delivery
    CARD = 'CARD'

class Order(models.Model):
    city = models.CharField(max_length=400, default="",blank=False)
    zip_code = models.CharField(max_length=100, default="",blank=False)
    street = models.CharField(max_length=500, default="",blank=False)
    state = models.CharField(max_length=100, default="",blank=False)
    country = models.CharField(max_length=100, default="",blank=False)
    phone_number = models.CharField(max_length=100, default="",blank=False)
    total_amount = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices, default=PaymentMethod.COD)
    status = models.CharField(max_length=60, choices=OrderStatus.choices, default=OrderStatus.PROCESSING)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id) # type: ignore

class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name='orderitems')
    name = models.CharField(max_length=200, default="", blank=False)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)

    def __str__(self):
        return str(self.name) 