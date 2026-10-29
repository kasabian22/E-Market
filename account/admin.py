from django.contrib import admin
from .models import CustomUser
from django.contrib.auth import get_user_model

# استدعاء موديل المستخدم بتاعك
User = get_user_model()

# إنشاء كلاس للتحكم في شكل عرض الموديل في صفحة الأدمن
class CustomUserAdmin(admin.ModelAdmin):
    # تحديد الأعمدة اللي هتظهر في القائمة
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

# تسجيل الموديل مع الكلاس الجديد
admin.site.register(User, CustomUserAdmin)