from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

app_name = "orders"

urlpatterns = [
    # path("", views.OrderViewSet.as_view(), name="orders"),
]

router = DefaultRouter()
router.register('', views.OrderViewSet)
urlpatterns += router.urls