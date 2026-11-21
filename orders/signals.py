from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Order)
def invalidate_orders_list_cache(sender, instance, **kwargs):
    """
    Invalidate orders list for a specific user's caches when a order is created, updated, deleted
    """
    if instance.user:
        # Increment the user's version number!
        cache.incr(f"user_version_{instance.user.id}")
        print(f"Bumped cache version for user {instance.user.id}")

    