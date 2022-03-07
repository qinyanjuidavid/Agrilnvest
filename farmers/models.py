from django.db import models
# from accounts.models import User
from django.utils.translation import gettext as _
# Create your models here.


class ProductCategory(models.Model):
    category = models.CharField(_("category"), max_length=89, unique=True)

    def __str__(self):
        return str(self.category)

    class Meta:
        verbose_name_plural = "Products Categories"
