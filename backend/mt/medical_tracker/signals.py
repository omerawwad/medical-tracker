from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Drug
@receiver([post_save, post_delete], sender=Drug)
def invalidate_product_cache(sender, instance, **kwargs):
	cache.delete_pattern('*drug_list*')