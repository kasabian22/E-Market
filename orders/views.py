from rest_framework.response import Response
from .serializers import OrderSerializer
from .models import Order
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

# Create your views here.
@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)