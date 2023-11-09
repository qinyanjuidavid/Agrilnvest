from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from modules.accounts.api.views import (
    GoogleSocialLoginViewSet,
    LoginViewSet,
    LogoutViewSet,
    RefreshViewSet,
    RegisterViewSet,
    UserViewSet,
)


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet, basename="users")
router.register("login", LoginViewSet, basename="login")
router.register("logout", LogoutViewSet, basename="logout")
router.register("auth-refresh", RefreshViewSet, basename="authRefresh")
router.register("register", RegisterViewSet, basename="register")
router.register(
    "google-sign-in",
    GoogleSocialLoginViewSet,
    basename="google-sign-in",
)


app_name = "api"
urlpatterns = router.urls
