from django.shortcuts import render

from modules.accounts.models import FarmProductCategory, Farmer
from modules.inventory.filters import FarmerFilter

# Create your views here.


def HomeView(request):
    farmer = Farmer.objects.all().order_by("?")
    farmers_count = Farmer.objects.values("specialization").count()
    product_category = FarmProductCategory.objects.all()
    farmerFilter = FarmerFilter(request.GET, queryset=farmer)
    context = {
        "dealers_count": farmers_count,
        "filter": farmerFilter,
        "categories": product_category,
    }
    return render(request, "farmers/home.html", context)
