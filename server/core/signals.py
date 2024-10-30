from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Field

@receiver(post_save, sender=Field)
def update_location(sender, instance, created, **kwargs):
    if created:
        instance.apply_coordinates()
        instance.save()
