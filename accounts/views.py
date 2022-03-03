from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from accounts.models import User
from accounts.decorators import (
    administrator_required, customer_required,
    dealer_required)


def dealers_profile_view(request):
    context = {

    }
    return render(request, "accounts/dealersProfile.html", context)


# class dealerSignupView(CreateView):
#     model = User
#     # form_class =
#     template_name = "accounts/signup.html"


def dealerSignupView(request):
    context = {}
    return render(request, "accounts/signup.html", context)


class adminSignupView(CreateView):
    model = User
    # form_class =
    template_name = "accounts/adminSignup.html"
