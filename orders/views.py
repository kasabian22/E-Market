from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import OrderFilter
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    # this is a way to cutomize the viewset and show defferent results with different url
    # @action(detail=False, methods=['get'], url_path='user-orders')
    # def user_orders(self, request):
    #     orders = self.get_queryset().filter(user=request.user)
    #     serializer = self.get_serializer(orders, many=True)
    #     return Response(serializer.data)

