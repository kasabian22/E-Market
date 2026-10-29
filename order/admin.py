from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    # تحديد الأعمدة اللي هتظهر في القائمة
    list_display = ('user', 'city', 'zip_code', 'street', 'state', 'country', 'phone_number', 'total_amount', 'payment_status', 'payment_method', 'status', 'date_created')
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'name', 'quantity', 'price')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)