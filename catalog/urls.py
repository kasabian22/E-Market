from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.ProductListCreateAPIView.as_view(), name='ProductListAPIView'),
    path('product/<slug:slug>/', views.ProductDetailAPIView.as_view(), name='view-product'),
    # path('product/create/', views.ProductCreateAPIView.as_view(), name='create-product'),
]
