from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Order
from rest_framework import status

class UserOrderTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='test')
        user2 = User.objects.create_user(username='user2', password='test')
        Order.objects.create(user=user1, subtotal=100.00, shipping_cost=10.00, total_cost=110.00, customer_name='User One', phone_number='1234', city='City', address='Street 1')
        Order.objects.create(user=user2, subtotal=100.00, shipping_cost=10.00, total_cost=110.00, customer_name='User One', phone_number='1234', city='City', address='Street 1')

    def test_user_order_endpoint_retrievees_only_authenticated_user_orders(self):
        user = User.objects.get(username='user1')
        self.client.force_login(user)
        response = self.client.get(reverse('orders:orders'))

        # check if the user trying to view the page is authenticated
        assert response.status_code == status.HTTP_200_OK
        orders = response.json()

        # check that the orders relate to the authenticated user
        self.assertTrue(all(order['user'] == user.id for order in orders))

    def test_user_order_list_unauthenticated(self):
        # trying to open the orders page without authentication
        response = self.client.get(reverse('orders:orders'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)