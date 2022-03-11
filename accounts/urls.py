from django.contrib.auth import views as auth_views
from django.urls import path

from accounts import views
from accounts.views import (
    dealerSignupView, adminSignupView,
    customerSignupView)

app_name = "accounts"
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name="accounts/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(
        template_name="accounts/logout.html"), name="logout"),
    path("signup/", dealerSignupView.as_view(), name="dealerSignup"),
    path("customer/signup/", customerSignupView.as_view(),
         name="customerSignup"),
    path("administrator/signup/", adminSignupView.as_view(),
         name="adminSignup"),
    # Password Reset
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password_reset.html",
             success_url='/accounts/password_reset/done/',
             email_template_name="accounts/password_reset_email.html",
             subject_template_name="accounts/password_reset_subject.txt"),
         name="password_reset"),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html",),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password_reset_confirm.html",
             success_url='/reset/done/'
         ),
         name="password_reset_confirm"
         ),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"),
        name="password_reset_complete"),

    # Profile
    path("farmer/profile/", views.Farmer_Profile_View,
         name="farmerProfile"),
    path('customer/profile/', views.Customer_Profile_View,
         name="customerProfile"),
    path('administrator/profile/', views.administrator_Profile_View,
         name="administratorProfile"),
]
