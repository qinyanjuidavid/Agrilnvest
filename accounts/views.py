from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from accounts.models import User
from accounts.decorators import (
    administrator_required, customer_required,
    dealer_required)
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.files.base import File
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView
from accounts.tokens import account_activation_token
from accounts.forms import UserSignUpForm
from accounts.sendMails import send_activation_mail


def dealers_profile_view(request):
    context = {

    }
    return render(request, "accounts/dealersProfile.html", context)


class dealerSignupView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = "accounts/dealerSignup.html"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Dealer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "Dealer"
            user.save()
            send_activation_mail(user, self.request)
        return render(self.request, "accounts/sign_alert.html")


class adminSignupView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = "accounts/adminSignup.html"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Administrator'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = True
            user.is_staff = True
            user.role = "Administrator"
            user.save()
            send_activation_mail(user, self.request)
        return render(self.request, "accounts/sign_alert.html")


class customerSignupView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = "accounts/customerSignup.html"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "Customer"
            user.save()
            send_activation_mail(user, self.request)
        return render(self.request, "accounts/sign_alert.html")


def Farmer_Profile_View(request):
    context = {

    }
    return render(request, "accounts/farmerProfile.html", context)


def Customer_Profile_View(request):
    context = {

    }
    return render(request, "accounts/customerProfile.html", context)


def administrator_Profile_View(request):
    context = {

    }
    return render(request, "accounts/administratorProfile.html", context)
