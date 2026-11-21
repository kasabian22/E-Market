from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.core.cache import cache
from rest_framework.response import Response

from .filters import OrderFilter
from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer


def get_user_cache_version(user_id):
    # Returns the current version, defaults to 1 if not set
    return cache.get_or_set(f"user_version_{user_id}", 1, timeout=None)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    # auto assign the user
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        # changing the serializer based on the request
        # you can also check if POST: if self.request.method == 'POST'
        if self.action == 'create':
            return OrderCreateSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        version = get_user_cache_version(user_id)
        
        # This key automatically handles query params (filters, pagination, sorting)!
        query = request.META.get('QUERY_STRING', '')
        cache_key = f"orders_u{user_id}_v{version}_{query}"
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return Response(cached_response)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 60 * 2)
        return response
    
    @method_decorator(cache_page(60 * 60 * 2, key_prefix="orders_list"))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # this is another way to cutomize the viewset and show defferent results with different url
    # @action(detail=False, methods=['get'], url_path='user-orders')
    # def user_orders(self, request):
    #     orders = self.get_queryset().filter(user=request.user)
    #     serializer = self.get_serializer(orders, many=True)
    #     return Response(serializer.data)

