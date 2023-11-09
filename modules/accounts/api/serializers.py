from django.contrib.auth import get_user_model
from modules.accounts.models import RoleChoices
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for the User model.

    Args:
        serializers.ModelSerializer: Inherits from the Django REST Framework
        ModelSerializer class.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "phone_no",
            "is_staff",
            "is_active",
            "is_superuser",
            "role",
            "timestamp",
            "deleted_at",
            "updated_at",
        ]

        extra_kwargs = {
            "phone_no": {"validators": []},
            "email": {"validators": []},
        }

        read_only_fields = (
            "email",
            "role",
        )


class LoginSerializer(TokenObtainPairSerializer):
    """
    Serializer for user login and token generation.

    This serializer is responsible for generating JWT tokens upon user login.

    Returns:
        A dictionary containing user data, refresh token, and access token.
    """

    def validate(self, attrs):
        """
        Validate user credentials and generate JWT tokens.

        Args:
            attrs (dict): Dictionary containing user credentials.

        Returns:
            dict: A dictionary containing user data, refresh token, and access token.
        """
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["user"] = UserSerializer(self.user).data
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            # Update user's last login timestamp
            self.user.last_login = timezone.now()
            self.user.save()

        return data


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Example:
        data = {
            "phone_no": "1234567890",
            "email": "user@example.com",
            "name": "John Doe",
            "password": "strongpassword",
            "password_confirmation": "strongpassword"
        }
    """

    password = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True,
        style={"input_type": "password"},
        required=True,
        validators=[validate_password],  # Enforce password validation
    )
    password_confirmation = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True,
        style={"input_type": "password"},
        required=True,
    )
    email = serializers.EmailField(
        required=True,
        max_length=128,
    )
    name = serializers.CharField(max_length=255, required=True)
    phone_no = serializers.CharField(max_length=25, required=True)

    class Meta:
        model = User
        fields = (
            "phone_no",
            "email",
            "name",
            "password",
            "password_confirmation",
        )

    def validate(self, data):
        password1 = data.get("password")
        password2 = data.get("password_confirmation")

        if password1 != password2:
            raise serializers.ValidationError(
                {"error": "Passwords do not match."},
            )

        # Check if a user with the same email already exists
        if User.objects.filter(email=data.get("email")).exists():
            raise serializers.ValidationError(
                {
                    "error": "User with this email already exists.",
                },
            )

        return data

    def create(self, validated_data):
        phone_no = validated_data.get("phone_no")
        email = validated_data.get("email")
        name = validated_data.get("name")
        password = validated_data.get("password")

        # Check if a user with the same phone number already exists
        if User.objects.filter(phone_no=phone_no).exists():
            raise serializers.ValidationError(
                {"error": "User with this phone number already exists."},
            )

        user = User(
            phone_no=phone_no,
            email=email,
            name=name,
            # role=RoleChoices.,
            is_active=True,
        )
        user.set_password(password)
        user.save()
        return user
