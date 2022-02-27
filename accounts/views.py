from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView


def dealers_profile_view(request):
    context = {

    }
    return render(request, "accounts/dealersProfile.html", context)


def customer_profile_view(request):
    context = {

    }
    return render(request, "accounts/customerProfile.html", context)


class customerSignupView(CreateView):
    pass


class dealerSignupView(CreateView):
    pass


class adminSignupView(CreateView):
    pass
