import requests

from django.contrib.auth import get_user_model
from modules.accounts.permissions import IsSuperUser
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.core.exceptions import ValidationError
from modules.accounts.api.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)
from django.core.validators import validate_email


User = get_user_model()


class LoginViewSet(ModelViewSet, TokenObtainPairView):
    """
    API endpoint for user login and obtaining access and refresh tokens.
    """

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except ValidationError as e:
            return Response(
                {"error": e.args[0]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutViewSet(ModelViewSet):
    """
    Logout view to invalidate the user's refresh token.
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Blacklist the refresh token, making it invalid
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"success": "User was successfully logged out."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RefreshViewSet(ModelViewSet, TokenRefreshView):
    """
    Endpoint allows all users to refresh their token,
    by passing the refresh token in order to get a new access token
    """

    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegisterViewSet(ModelViewSet):
    """
    ViewSet for user registration.

    Allows users to register by providing necessary information
    such as phone number, email, name, and password.
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        context = {"request": request}
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            response_data = {
                "user": serializer.data,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Google Login
# https://www.googleapis.com/auth/userinfo.email
# https://developers.google.com/oauthplayground/
class GoogleSocialLoginViewSet(ModelViewSet):
    """
    Google Social Login, Use the url below to test the endpoint;
    https://www.googleapis.com/auth/userinfo.email
    https://developers.google.com/oauthplayground/
    return access_token from the url above
    """

    permission_classes = [AllowAny]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        token = request.data.get("token")

        if not token:
            return Response(
                {"error": "Token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            response = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                params={"access_token": token},
            )
            response.raise_for_status()
            response_data = response.json()

            email = response_data.get("email")
            if not email:
                return Response(
                    {"error": "Email not provided by Google"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Validate email address format
            try:
                validate_email(email)
            except ValidationError:
                return Response(
                    {"error": "Invalid email address"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user, created = User.objects.get_or_create(email=email)
            if created:
                user.full_name = response_data.get("name", "")
                user.is_active = True
                user.set_unusable_password()
                user.save()

            token = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(token),
                    "access": str(token.access_token),
                },
                status=status.HTTP_200_OK,
            )
        except requests.HTTPError as e:
            return Response(
                {"error": f"Google API request failed: {e.response.text}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed, created, updated, or deleted.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSuperUser]
    http_method_names = ["get", "post", "put", "patch", "delete"]
