from django_filters import rest_framework as filters
from rest_framework import generics

from .models import Product
from .serializers import ProductSerializer

# Custom Filter
# class InStockFilterBackend(filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         in_stock = request.query_params.get('in_stock')
#         # If the frontend sent ?in_stock=true
#         if in_stock in ['true', '1']:
#             return queryset.filter(stock_quantity__gt=0)
        
#         # If not sent or false, don't filter out-of-stock items
#         return queryset



class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    in_stock = filters.BooleanFilter(method='filter_in_stock')

    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'], 
            'price': ['exact', 'lt', 'gt', 'range'], 
            # 'category': , 
            }
    def filter_in_stock(self, queryset, name, value):
        if value:  # if value is True (?in_stock=true)
            return queryset.filter(stock_quantity__gt=0)
        return queryset

