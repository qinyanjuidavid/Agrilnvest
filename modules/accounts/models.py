from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group

from modules.accounts.managers import UserManager
from django.core.mail import send_mail


class Constants(models.TextChoices):
    """
    A class to define constants YES and NO for flag fields.
    """

    YES = "Yes", ("Yes")
    NO = "No", ("No")


class TrackingModel(models.Model):
    """
    Abstract base model for tracking creation and update timestamps.
    """

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_added_by",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_updated_by",
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_deleted_by",
    )

    updated_flag = models.CharField(
        _("updated flag"),
        max_length=3,
        choices=Constants.choices,
        default=Constants.NO,
    )
    deleted_flag = models.CharField(
        _("deleted flag"),
        max_length=3,
        choices=Constants.choices,
        default=Constants.NO,
    )
    deleted_at = models.DateTimeField(_("deleted at"), null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if "request" in kwargs:
            self.request = kwargs.pop("request")
        super(TrackingModel, self).save(*args, **kwargs)


class RoleChoices(models.TextChoices):
    """
    Enumeration of possible user roles.
    """

    SUPERUSER = "SUPERUSER", ("SUPERUSER")
    CUSTOMER = "CUSTOMER", ("CUSTOMER")
    FARMER = "FARMER", ("FARMER")


class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    """
    Custom User model representing a user of the application.
    """

    name = models.CharField(_("full name"), blank=True, max_length=255)
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": ("A user with that email already exists."),
        },
    )
    phone_no = models.CharField(
        _("phone number"),
        max_length=56,
        blank=True,
        null=True,
    )
    is_staff = models.BooleanField(_("staff"), default=False)
    is_active = models.BooleanField(_("active"), default=False)
    is_superuser = models.BooleanField(_("superuser"), default=False)
    role = models.CharField(
        _("role"),
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.CUSTOMER,
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_("The groups this user belongs to."),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set",
        related_query_name="user",
    )
    timestamp = models.DateTimeField(_("date joined"), auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name_plural = "users"
        ordering = ["-id"]

    def __str__(self):
        """
        Returns a string representation of the user object.

        Returns:
            str: The user's email address.
        """
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to the user.

        Args:
            subject (str): The subject of the email.
            message (str): The content of the email.
            from_email (str, optional): The sender's email address.
            Defaults to None.
            **kwargs: Additional keyword arguments accepted by Django's
            `send_mail` function.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def superuser(self):
        """
        Property indicating whether the user is a superuser.

        Returns:
            bool: True if the user is a superuser, False otherwise.
        """
        return self.is_superuser

    @property
    def staff(self):
        """
        Property indicating whether the user is a staff member.

        Returns:
            bool: True if the user is a staff member, False otherwise.
        """
        return self.is_staff

    @property
    def active(self):
        """
        Property indicating whether the user account is active.

        Returns:
            bool: True if the user account is active, False otherwise.
        """
        return self.is_active


class Coordinates(models.Model):
    """
    Abstract Model representing GPS coordinates.
    """

    latitude = models.FloatField(_("latitude"), default=-1.286389)
    longitude = models.FloatField(_("longitude"), default=36.817223)

    class Meta:
        abstract = True


class GenderChoices(models.TextChoices):
    """
    Enumeration of possible gender choices for individuals.
    """

    MALE = "M", _("Male")
    FEMALE = "F", _("Female")
    PREFER_NOT_TO_SAY = "P", _("Prefer not to say")


class Profile(Coordinates):
    """
    User profile
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_profile",
    )

    profile_image = models.ImageField(
        _("profile picture"),
        upload_to="profile_images",
        null=True,
        blank=True,
        default="default.png",
    )
    bio = models.TextField(_("bio"), max_length=500, null=True, blank=True)
    gender = models.CharField(
        _("gender"),
        max_length=1,
        choices=GenderChoices.choices,
        default=GenderChoices.PREFER_NOT_TO_SAY,
    )
    county = models.CharField(_("county"), max_length=100, blank=True, null=True)
    town = models.CharField(_("town"), max_length=100, blank=True, null=True)
    estate = models.CharField(_("estate"), max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)

    def __str__(self):
        return self.user.email

    class Meta:
        abstract = True


class SuperUser(Profile):
    """
    Model representing app Superusers.
    """

    def __str__(self):
        return self.user.email or self.user.phone_no

    class Meta:
        verbose_name_plural = "Super Users"
        ordering = ["-id"]


class Customer(Profile):
    """
    Model representing app Customers.
    """

    def __str__(self):
        return self.user.email or self.user.phone_no

    class Meta:
        verbose_name_plural = "Customers"
        ordering = ["-id"]


class FarmProductCategory(TrackingModel):
    """
    Represents the categories of farm products available on the platform.
    """

    category_name = models.CharField(
        _("category"),
        max_length=89,
        unique=True,
    )
    category_icon = models.ImageField(
        upload_to="crops_icons/",
        blank=True,
        null=True,
    )
    description = models.TextField(_("description"), blank=True, null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Farm Product Categories"
        ordering = ["-id"]


class ResponseTimeChoices(models.TextChoices):
    """
    Enumeration representing response time choices for farmers.
    """

    TWO_HOURS = "2 Hrs", _("2 Hrs")
    SIX_HOURS = "6 Hrs", _("6 Hrs")
    ONE_DAY = "1 day", _("1 day")
    TWO_DAYS = "2+ Days", _("2+ Days")


class DeliveryLevel(models.TextChoices):
    """
    Enumeration representing delivery level choices for farmers.
    """

    BEGINNER = "BEGINNER", _("BEGINNER")
    AMATEUR = "AMATEUR", _("AMATEUR")
    PRO = "PRO", _("PRO")


class Farmer(Profile):
    """
    Represents a farmer user profile on the platform.
    """

    is_verified = models.BooleanField(_("verified"), default=True)
    protect_email = models.BooleanField(_("protect email"), default=True)
    level = models.CharField(
        _("level"),
        max_length=20,
        choices=DeliveryLevel.choices,
        default=DeliveryLevel.BEGINNER,
    )
    response_time = models.CharField(
        _("response_time"),
        max_length=20,
        choices=ResponseTimeChoices.choices,
        default=ResponseTimeChoices.TWO_HOURS,
    )
    specialization = models.ForeignKey(
        FarmProductCategory,
        related_name="categories",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.email or self.user.phone_no

    class Meta:
        verbose_name_plural = "Farmers"
        ordering = ["-id"]
