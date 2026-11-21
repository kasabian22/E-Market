from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "catalog"
router = DefaultRouter()

urlpatterns = [
    # path("", views.ProductListCreateAPIView.as_view(), name="ProductListAPIView"),
    # path(
    #     "products/<slug:slug>/",
    #     views.ProductDetailAPIView.as_view(),
    #     name="view-product",
    # ),
    # path('product/create/', views.ProductCreateAPIView.as_view(), name='create-product'),
]

router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')
urlpatterns += router.urls