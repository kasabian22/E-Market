import django_filters
from .models import Product

class ProductsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    # keyword searches with the part of the name of the "field_name" you choose
    keyword = django_filters.filters.CharFilter(field_name="name", lookup_expr="icontains")
    # gte means greater than or equal
    minPrice = django_filters.filters.NumberFilter(field_name="price" or 0, lookup_expr="gte")
    # lte means less than or equal
    maxPrice = django_filters.filters.NumberFilter(field_name="price" or 10000, lookup_expr="lte")


    class Meta:
        model = Product
        # fields = ['category', 'brand']
        fields = ('category', 'brand', 'price', 'keyword', 'minPrice', 'maxPrice')