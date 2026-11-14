import uuid
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total cost of items before shipping and taxes")
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Shipping cost")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total cost of the order")
    customer_name = models.CharField(max_length=255, help_text="Name of the customer")
    phone_number = models.CharField(max_length=20, help_text="Customer's phone number")
    city = models.CharField(max_length=100, help_text="City of the customer")
    address = models.TextField(help_text="Full address of the customer")
    notes = models.TextField(blank=True, null=True, help_text="Additional notes or instructions for the order")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_number} for {self.user.username}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the product at the time of order")


    @property
    def item_subtotal(self):
        return self.price * self.quantity
    
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.order_number}"
    