from rest_framework import serializers
from .models import Order, OrderItem
from catalog.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'price', 'item_subtotal')


class OrderSerializer(serializers.ModelSerializer):
    # items must match order related name in the OrderItem model
    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = ['user', 'status', 'order_number', 'subtotal', 'shipping_cost', 'total_cost', 'customer_name', 'phone_number', 'city', 'address', 'notes', 'created_at', 'items']

