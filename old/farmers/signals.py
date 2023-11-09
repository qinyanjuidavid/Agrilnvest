from django.db.models.signals import (
    post_save,
    post_migrate)
from django.conf import settings
from django.dispatch import receiver
from farmers.models import ProductCategory
from accounts.models import User
import os


@receiver(post_save, sender=User)
def createProductCategory(sender, instance, created, *args, **kwargs):
    if created:
        cropIcon = os.listdir(os.path.join(settings.MEDIA_ROOT, "crops_icons"))
        for category in cropIcon:
            crop_name, label = category.split(".")
            if ProductCategory.objects.filter(
               category=crop_name
               ).exists():
                pass
            else:
                icons_dir = f"crops_icons/{crop_name}.{label}"
                ProductCategory.objects.update_or_create(
                    category=crop_name,
                    crop_icon=icons_dir
                )
