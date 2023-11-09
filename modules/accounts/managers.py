from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager for User model.
    """

    def _create_user(self, email, password=None, **extra_fields):
        """
        Create and return a user with an email address and password.

        Args:
            email (str): User's email address.
            password (str): User's password.
            **extra_fields: Additional fields to be saved in the user model.

        Returns:
            User: Created user instance.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create a regular user with the given email and password.

        Args:
            email (str): User's email address.
            password (str): User's password.
            **extra_fields: Additional fields to be saved in the user model.

        Returns:
            User: Created regular user instance.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create a superuser with the given email and password.

        Args:
            email (str): User's email address.
            password (str): User's password.
            **extra_fields: Additional fields to be saved in the user model.

        Returns:
            User: Created superuser instance.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "SUPERUSER")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
