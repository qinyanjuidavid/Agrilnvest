from urllib import response
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import validators
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext as _
from farmers.models import ProductCategory


class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Tracking Model"


class CustomManager(BaseUserManager):
    def create_user(self, email, username, password=None,
                    role="Administrator",
                    is_active=True, is_admin=False,
                    is_staff=False):
        if email is None:
            raise ValueError("Users must have an email!")
        if password is None:
            raise ValueError("Users must have a password!")
        if username is None:
            raise ValueError("Users must have a username!")
        user_obj = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user_obj.set_password(password)
        user_obj.role = "Administrator"
        user_obj.is_active = is_active
        user_obj.is_admin = is_admin
        user_obj.is_staff = is_staff
        user_obj.save(using=self._db)

        return user_obj

    def create_staff(self, email, username, password=None):
        user = self.create_user(
            email, username, password=password,
            role="Administrator",
            is_active=True, is_admin=False,
            is_staff=True
        )
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email, username, password=password,
            is_staff=True, is_admin=True, is_active=True,
            role="Administrator",
        )
        return user


class User(AbstractBaseUser, TrackingModel):
    username_validator = UnicodeUsernameValidator()
    role_choice = (
        ("Administrator", "Administrator"),
        ("Customer", "Customer"),
        ("Dealer", "Dealer"),
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': ('A user with that username already exists.')
        }
    )
    full_name = models.CharField(
        _('full name'), max_length=150, blank=True, null=True)
    phone = PhoneNumberField(_('phone number'),
                             unique=True, blank=True,
                             null=True, max_length=27)
    email = models.EmailField(_('email address'), unique=True,
                              error_messages={
        'unique': ('A user with that email already exists.')
    }
    )
    is_active = models.BooleanField(_("active"), default=True)
    is_admin = models.BooleanField(_("admin"), default=False)
    is_staff = models.BooleanField(_("staff"), default=False)
    role = models.CharField(_("role"), max_length=56, choices=role_choice)
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)

    def __str__(self):
        return self.username

    objects = CustomManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def admin(self):
        return self.admin

    @property
    def staff(self):
        return self.staff

    @property
    def active(self):
        return self.active


class Counties(models.Model):
    county = models.CharField(_("county"), max_length=40, unique=True)

    def __str__(self):
        return self.county

    class Meta:
        verbose_name_plural = "Counties"
        ordering = ["-id", ]


class ResponseTime(models.Model):
    response = models.CharField(_("response time"),
                                max_length=15,
                                unique=True
                                )

    def __str__(self):
        return self.response

    class Meta:
        verbose_name_plural = "Response Time"


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE, unique=True)
    bio = models.TextField(_("bio"), blank=True, null=True)
    profile_picture = models.ImageField(
        _("profile picture"), upload_to="picture/%y/%m/%d",
        default="default.png")
    county = models.ForeignKey(Counties, on_delete=models.DO_NOTHING,
                               blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    estate = models.CharField(max_length=106, blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ["-id"]

    def __str__(self):
        return self.user.username


class Administrator(Profile):
    job_id = models.CharField(max_length=14, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Customer(Profile):
    pass

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name_plural = "Customers"
        ordering = ["-id"]


class Dealer(Profile):
    derivery_choices = (
        ("Free", "Free"),
        ("Paid", "Paid")
    )
    delivery_level = (
        ("Beginner", "Beginner"),
        ("Ameture", "Ameture"),
        ("Pro", "Pro")
    )
    response_time = (
        ("2 hrs", "2 hrs"),
        ("6 hrs", "6 hrs"),
        ("1 day", "1 day"),
        ("2+ days", "2+ days")
    )
    category = models.ForeignKey(
        ProductCategory, related_name="categories",
        on_delete=models.CASCADE, blank=True, null=True)
    approve = models.BooleanField(_("approve"), default=True)
    protect_email = models.BooleanField(_("protect email"),
                                        default=True)
    derivery = models.CharField(
        _("derivery"), max_length=10,
        choices=derivery_choices,
        blank=True, null=True
    )
    level = models.CharField(
        _("delivery level"), max_length=14,
        choices=delivery_level,
        blank=True, null=True
    )
    response = models.ForeignKey(ResponseTime,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True)

    def __str__(self):
        return str(self.user.username)
