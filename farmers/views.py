from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from accounts.models import Dealer, User
from farmers.filters import OrderFilter
from farmers.models import ProductCategory


def homeView(request):
    dealerQs = Dealer.objects.all().order_by("?")
    categoriesQuery = ProductCategory.objects.all()
    orderFilter = OrderFilter(request.GET, queryset=dealerQs)

    context = {
        "filter": orderFilter,
        "categories": categoriesQuery
    }
    return render(request, "farmers/home.html", context)


def CategoryFilterView(request, category):
    dealerQs = Dealer.objects.filter(
        category__category=category
    ).order_by("?")
    categoriesQuery = ProductCategory.objects.all()
    orderFilter = OrderFilter(request.GET, queryset=dealerQs)
    context = {
        "filter": orderFilter,
        "categories": categoriesQuery
    }
    return render(request, "farmers/categoryFilter.html", context)


def suppliers_category(request):
    context = {

    }
    return render(request, "farmers/category.html", context)


def SupportView(request):
    context = {

    }
    return render(request, "farmers/support.html", context)


def supplierDetailsView(request, username):
    context = {

    }
    return render(request, "farmers/supplierDetails.html", context)


def supplierCategoryView(request):
    context = {

    }
    return render(request, "farmers/category.html", context)


def productAddView(request):
    context = {

    }
    return render(request, "farmers/product_add.html", context)


def dealersDetailsView(request):
    context = {

    }
    return render(request, "farmers/dealerDetails.html", context)
