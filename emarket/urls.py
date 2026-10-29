"""
URL configuration for emarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from utils.error_view import handler404 as custom_handler404, handler500 as custom_handler500
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls', namespace='products')),
    path('api/', include('account.urls', namespace='account')),
    path('api/', include('order.urls', namespace='order')),
    path('api/token/', TokenObtainPairView.as_view())
]

handler404 = custom_handler404
handler500 = custom_handler500