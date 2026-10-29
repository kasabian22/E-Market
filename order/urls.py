from django.urls import path
from . import views

app_name = 'project'   
urlpatterns = [
    path('orders/new/', views.new_order, name='new_order'),
    path('orders/', views.get_orders, name='get_orders'),
    path('order/<str:pk>/', views.get_order, name='get_order'),
    path('order/<str:pk>/edit/', views.edit_order, name='edit_order'),
    path('order/<str:pk>/delete/', views.delete_order, name='delete_order'),
]