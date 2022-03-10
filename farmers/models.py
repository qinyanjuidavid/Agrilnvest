from django.db import models
from accounts.models import Farmer, TrackingModel
from django.utils.translation import gettext as _
# Create your models here.


class ProductCategory(models.Model):
    category = models.CharField(_("category"), max_length=89, unique=True)
    crop_icon = models.ImageField(
        upload_to="crops-icons/", blank=True, null=True)

    def __str__(self):
        return str(self.category)

    class Meta:
        verbose_name_plural = "Products Categories"


class Product(models.Model):
    item = models.CharField(_("item"), max_length=157)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    quantity = models.FloatField(
        default=0.00, help_text="Number of Kgs available")
    image = models.ImageField(upload_to="products/%y%m/%d")
    price = models.FloatField(_("price"))
    timestamp = models.ForeignKey(TrackingModel,
                                  on_delete=models.DO_NOTHING)
    approve = models.BooleanField(_("approve"), default=True)
    description = models.TextField(_("description"), blank=True, null=True)
    on_stock = models.BooleanField(_("on stock"), default=True)

    def __str__(self):
        return str(self.item)

    class Meta:
        verbose_name_plural = "Products"
