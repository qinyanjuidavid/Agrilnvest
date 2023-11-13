from django.db import models
from django.utils.translation import gettext_lazy as _

from modules.accounts.models import Farmer, FarmProductCategory


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(_("product name"), max_length=156)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    quantity = models.FloatField(
        default=0.00,
        help_text="Number of Kgs available",
    )
    image = models.ImageField(upload_to="products/%y%m/%d")
    price = models.FloatField(_("price"), default=0.00)
    is_verified = models.BooleanField(_("is_verified"), default=True)
    description = models.TextField(_("description"), blank=True, null=True)
    on_stock = models.BooleanField(_("on stock"), default=True)
    category = models.ForeignKey(
        FarmProductCategory,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name_plural = "Farm Products"
