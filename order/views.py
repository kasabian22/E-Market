from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from products.models import Product
from .serializers import OrderSerializer
from .models import OrderItem, Order
from django.db.models import Avg
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response({'orders': serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    serializer = OrderSerializer(order, many=False)
    return Response({'order': serializer.data})

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def edit_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.status = request.data['status']
    order.save()
    serializer = OrderSerializer(order, many=False)
    return Response({'order': serializer.data})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.delete()
    return Response({'details': 'Order Got deleted!'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order (request):
    data = request.data
    user = request.user
    order_items = data['order_Items']

    if order_items and len(order_items) == 0:
        return Response({'error': 'No order recieved!'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        total_amount = sum(item['price'] * item['quantity'] for item in order_items)
        order = Order.objects.create(
            user = user,
            city = data['city'],
            zip_code = data['zip_code'],
            street = data['street'],
            state = data['state'],
            country = data['country'],
            phone_number = data['phone_number'],
            total_amount = total_amount,
        )

        for i in order_items:
            product = Product.objects.get(id=i['product'])
            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                quantity = i['quantity'],
                price = i['price']
            )
            product.stock -= item.quantity
            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
