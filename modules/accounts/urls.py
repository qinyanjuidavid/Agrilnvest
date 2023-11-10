from django.contrib.auth import views as auth_views
from django.urls import path

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        auth_views.LogoutView.as_view(
            template_name="accounts/login.html",
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="modules/accounts/logout.html",
        ),
        name="logout",
    ),
    # path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="modules/accounts/password_reset.html",
            success_url="/accounts/password_reset/done/",
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="modules/accounts/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="modules/accounts/password_reset_confirm.html",
            success_url="/reset/done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="modules/accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
