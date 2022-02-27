from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def homeView(request):
    context = {

    }
    return render(request, "farmers/home.html", context)


def welcomeView(request):
    context = {

    }
    return render(request, "farmers/welcome.html", context)


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
