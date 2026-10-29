from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class CustomUser(AbstractUser):
    # بنخلي الإيميل فريد (ممنوع التكرار)
    email = models.EmailField(unique=True)
    
    # بنقول لجانغو: الإيميل هو الحقل الأساسي لتسجيل الدخول بدل اليوزرنيم
    USERNAME_FIELD = 'email'
    
    # بنسيب اليوزرنيم مطلوب عشان لو حبيت تستخدمه كاسم عرض، وعشان دالة إنشاء السوبر يوزر
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE)
    reset_password_token  = models.CharField(max_length=50, default="", blank=True)
    reset_password_expire = models.DateTimeField(null=True, blank=True)

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, created, **kwargs):
    print(f"instance:{instance}")
    user = instance
    if created:
        profile = Profile(user = user)
        profile.save()

    

    