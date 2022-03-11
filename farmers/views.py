from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from accounts.models import Dealer, User, Rating, Product
from farmers.filters import OrderFilter
from farmers.forms import ProductAddForm, FarmerCategoryForm
from farmers.models import ProductCategory
from accounts.decorators import customer_required, dealer_required
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages


def homeView(request):
    dealerQs = Dealer.objects.all().order_by("?")
    dealers_count = (Dealer.objects.values(
        'category').count())

    categoriesQuery = ProductCategory.objects.all()
    orderFilter = OrderFilter(request.GET, queryset=dealerQs)
    context = {
        "dealers_count": dealers_count,
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
    dealers_count = (Dealer.objects.values(
        'category').count())
    context = {
        "filter": orderFilter,
        "categories": categoriesQuery,
        "dealers_count": dealers_count
    }
    return render(request, "farmers/categoryFilter.html", context)


def SupportView(request):
    context = {

    }
    return render(request, "farmers/support.html", context)


@login_required
@dealer_required
def productAddView(request):
    dealerQs = Dealer.objects.get(user=request.user)
    form = ProductAddForm()
    category = dealerQs.category
    initial_data = {
        "category": category,
    }
    categoryForm = FarmerCategoryForm(initial=initial_data)

    if request.method == "POST":
        form = ProductAddForm(request.POST, request.FILES)
        if form.is_valid():
            qsForm = form.save(commit=False)
            qsForm.farmer = dealerQs
            qsForm.category = dealerQs.category
            qsForm.save()
            messages.success(request, "The product was successfully added.")
            return HttpResponseRedirect("/post/products/")
        else:
            form = ProductAddForm()
    context = {
        "form": form,
        "dealer": dealerQs,
        "catForm": categoryForm

    }
    return render(request, "farmers/product_add.html", context)


def dealersDetailsView(request, username):
    dealerQs = Dealer.objects.get(
        user__username=username
    )
    context = {
        "dealer": dealerQs
    }
    return render(request, "farmers/dealerDetails.html", context)


@login_required
@customer_required
def rateFarmer(request):
    if request.method == "POST":
        customer_id = request.POST.get('customer_id')
        el_id = request.POST.get('el_id')
        val = request.POST.get('val')

        # get the dealer
        dealer = Dealer.objects.get(pk=el_id)

        # update a rating instance
        try:
            obj = Rating.objects.get(Q(dealer=dealer),
                                     Q(customer=request.user))

            obj.rate = val
            obj.save()
        except Rating.DoesNotExist:
            # create a rating
            obj = Rating(dealer=dealer, customer=request.user, rate=val)
            obj.save()
        return JsonResponse(
            {
                "Success": "true", "rate": val
            }, safe=False
        )
    return JsonResponse({"success": "false"})
