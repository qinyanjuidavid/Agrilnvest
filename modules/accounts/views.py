from django.shortcuts import render
from modules.accounts.decorators import customer_required, farmer_required

from modules.accounts.models import Customer, Farmer, RoleChoices, User
from django.views.generic import CreateView
from modules.accounts.forms import (
    CustomerProfileUpdateForm,
    FarmerProfileUpdateForm,
    FarmerSignupForm,
    UserSignupForm,
    UserUpdateForm,
)
from modules.accounts.send_mails import send_activation_mail
from django.contrib.auth import login
from modules.accounts.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect


class FarmerSignupView(CreateView):
    model = User
    form_class = FarmerSignupForm
    template_name = "accounts/farmerSignup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = RoleChoices.FARMER
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            send_activation_mail(user, self.request)
        return render(self.request, "accounts/sign_alert.html")


class CustomerSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = "accounts/customerSignup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = RoleChoices.CUSTOMER
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            send_activation_mail(user, self.request)
        return render(self.request, "accounts/sign_alert.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, "accounts/activate_success.html")
    else:
        return render(request, "accounts/activate_fail.html")


@login_required
@farmer_required
def FarmerProfileView(request):
    farmer = Farmer.objects.get(user=request.user)
    form = FarmerProfileUpdateForm(instance=farmer)
    user_form = UserUpdateForm(instance=request.user)

    if request.method == "POST":
        form = FarmerProfileUpdateForm(
            request.POST or None, request.FILES or None, instance=farmer
        )
        user_form = UserUpdateForm(
            request.POST or None, request.FILES or None, instance=request.user
        )
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, "Profile successfully updated.")
            return HttpResponseRedirect("/accounts/farmer/profile/")
    context = {"form": form, "userForm": user_form, "dealer": farmer}
    return render(request, "accounts/farmerProfile.html", context)


@login_required
@customer_required
def CustomerProfileView(request):
    customer = Customer.objects.get(user=request.user)
    form = CustomerProfileUpdateForm(instance=customer)
    user_form = UserUpdateForm(instance=request.user)

    if request.method == "POST":
        form = CustomerProfileUpdateForm(
            request.POST or None, request.FILES or None, instance=customer
        )

        user_form = UserUpdateForm(
            request.POST or None, request.FILES or None, instance=request.user
        )
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, "Profile successfully updated.")
            return HttpResponseRedirect("/accounts/customer/profile/")

    context = {"form": form, "userForm": user_form, "customerQs": customer}
    return render(request, "accounts/customerProfile.html", context)
