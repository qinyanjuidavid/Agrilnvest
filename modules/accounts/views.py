from django.shortcuts import render
from modules.accounts.decorators import farmer_required

from modules.accounts.models import Farmer, RoleChoices, User
from django.views.generic import CreateView
from modules.accounts.forms import FarmerSignupForm, UserSignupForm
from modules.accounts.send_mails import send_activation_mail
from django.contrib.auth import authenticate, login
from modules.accounts.tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.decorators import login_required


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
    pass
