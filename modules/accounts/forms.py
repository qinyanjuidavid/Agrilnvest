from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    """
    Custom form for changing user information in the Django admin panel.

    Inherits from:
        admin_forms.UserChangeForm: Django's default form for changing user information in the admin panel.

    Attributes:
        Meta (class): Subclass of admin_forms.UserChangeForm.Meta. Specifies metadata options for the form.
            - model (class): The User model associated with the form.
            - field_classes (dict): Custom field classes for form fields.
            Overrides the default EmailField class for the 'email' field.
    """

    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {
            "email": EmailField,
        }


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {
                "unique": _("This email has already been taken."),
            },
        }
