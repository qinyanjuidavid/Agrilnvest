from django.db import models
from django.utils.translation import gettext as _
from cloudinary.models import CloudinaryField

# Create your models here.


class ProductCategory(models.Model):
    category = models.CharField(_("category"), max_length=89, unique=True)
    crop_icon = models.ImageField(upload_to="crops_icons/", blank=True, null=True)
    # crop_icon = CloudinaryField("category")

    def __str__(self):
        return str(self.category)

    class Meta:
        verbose_name_plural = "Products Categories"
