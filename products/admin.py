from django.contrib import admin
from .models import Product, Review

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    # تحديد الأعمدة اللي هتظهر في القائمة
    list_display = ('name', 'user', 'description', 'price', 'brand', 'category', 'ratings', 'stock', 'date')
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'comment', 'date')


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)