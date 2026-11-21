from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .filters import ProductFilter


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

# view and create and update abd delete products 
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter,
    ]
    search_fields = ["category__name", "name", "description", "brand"]
    ordering_fields = ["id", "name", "description", "stock_quantity", "price"]
    pagination_class = PageNumberPagination
    page_size = 2
    lookup_field = "slug"
    
    # it's slug by default but if you changed the kwarg in the url path change it here too, because the default is the type of the lookup
    lookup_url_kwarg = "slug"

    # you can make the user choose the number of pruducts in each page and limit that number
    # page_size_query_param = 'size'
    # max_page_size = 4

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    @method_decorator(cache_page(60 * 60 * 2, key_prefix="products_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    


