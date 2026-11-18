from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .filters import ProductFilter


@api_view(["GET"])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter,
    ]
    search_fields = ["category__name" "name", "description", "brand"]
    ordering_fields = ["id", "name", "description", "stock_quantity", "price"]
    pagination_class = PageNumberPagination
    page_size = 2

    # you can make the user choose the number of pruduct in each page and limit that number
    # page_size_query_param = 'size'
    # max_page_size = 4

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# class ProductCreateAPIView(generics.CreateAPIView):
#     model = Product
#     serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = "slug"

    # it's slug by default but if you changed the kwarg in the url path change it here too, because the default is the type of the lookup
    lookup_url_kwarg = "slug"

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
