from django.contrib import admin
from accounts.models import (User, Administrator, Customer, Dealer, Counties)


admin.site.register(User)
admin.site.register(Administrator)
admin.site.register(Customer)
admin.site.register(Dealer)


@admin.register(Counties)
class CountyAdmin(admin.ModelAdmin):
    list_display = ("county",)
    readonly_fields = ["county", ]
