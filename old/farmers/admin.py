from django.contrib import admin
from farmers.models import ProductCategory
from accounts.models import Product


admin.site.register(ProductCategory)
admin.site.register(Product)
