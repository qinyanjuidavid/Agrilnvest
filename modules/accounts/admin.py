from django.contrib import admin

from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from modules.accounts.forms import UserAdminChangeForm, UserAdminCreationForm
from modules.accounts.models import Customer, FarmProductCategory, Farmer, SuperUser

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name", "phone_no")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "timestamp")}),
        (
            _("Tracking Info"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "added_by",
                    "updated_by",
                    "deleted_by",
                    "updated_flag",
                    "deleted_flag",
                    "deleted_at",
                ),
            },
        ),
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
        "timestamp",
        "last_login",
        "added_by",
        "updated_by",
        "deleted_by",
        "updated_flag",
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        readonly_fields.extend(["created_at", "updated_at", "deleted_at"])
        return readonly_fields

    list_display = ["email", "name", "role", "is_superuser", "timestamp"]
    list_filter = [
        "is_superuser",
        "is_active",
        "is_staff",
        "role",
        "deleted_flag",
    ]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


class ProfileAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Profile model.
    """

    list_display = [
        "get_email",
        "get_name",
        "get_phone_number",
        "get_timestamp",
    ]
    list_filter = ["gender"]
    ordering = ["id"]

    def get_name(self, obj):
        """
        Retrieve the name of the user associated with the profile.

        Args:
            obj (Profile): Profile instance.

        Returns:
            str: User's name.
        """
        return obj.user.name

    get_name.short_description = "Name"
    get_name.admin_order_field = "user__name"

    def get_email(self, obj):
        """
        Retrieve the email address of the user associated with the profile.

        Args:
            obj (Profile): Profile instance.

        Returns:
            str: User's email address.
        """
        return obj.user.email

    get_email.short_description = "Email Address"
    get_email.admin_order_field = "user__email"

    def get_timestamp(self, obj):
        """
        Retrieve the date joined timestamp of the user
        associated with the profile.

        Args:
            obj (Profile): Profile instance.

        Returns:
            datetime: User's date joined timestamp.
        """
        return obj.user.timestamp

    get_timestamp.short_description = "Date Joined"
    get_timestamp.admin_order_field = "user__timestamp"

    def get_phone_number(self, obj):
        """
        Retrieve the phone number of the user associated with the profile.

        Args:
            obj (Profile): Profile instance.

        Returns:
            str: User's phone number.
        """
        return obj.user.phone_no

    get_phone_number.short_description = "Phone Number"
    get_phone_number.admin_order_field = "user__phone_no"


@admin.register(SuperUser)
class SuperUserAdmin(ProfileAdmin):
    """
    Admin configuration for SuperUser model.
    """


@admin.register(Customer)
class CustomerAdmin(ProfileAdmin):
    """
    Customer configuration for Customer model
    """


@admin.register(Farmer)
class FarmerAdmin(ProfileAdmin):
    """
    Farmer configuration for Farmer models
    """


@admin.register(FarmProductCategory)
class FarmProductCategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the FarmProductCategory model.

    Inherits from:
        admin.ModelAdmin: Django's default admin configuration for models.

    Attributes:
        list_display (list): The fields to be displayed in the list view of the admin panel.
        ordering (list): The fields by which the displayed records are ordered in the admin panel.
    """

    list_display = ["category_name", "created_at", "updated_at"]
    ordering = ["id"]
