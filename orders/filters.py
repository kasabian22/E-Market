import django_filters
from django_filters import rest_framework as filters
from rest_framework import generics

from .models import Order
from .serializers import OrderSerializer

# Custom filter for the viewset
class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')

    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['lt', 'gt', 'exact'],
        }
        