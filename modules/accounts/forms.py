from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django import forms

from modules.accounts.models import Customer, FarmProductCategory, RoleChoices, Farmer

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
            "email": forms.EmailField,
        }


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": forms.EmailField}
        error_messages = {
            "email": {
                "unique": _("This email has already been taken."),
            },
        }


class UserSignupForm(forms.ModelForm):
    """
    A form for user registration/signup.
    """

    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=156, required=True)
    phone = forms.CharField(max_length=20, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_confirmation = forms.CharField(
        label="Password Confirmation", widget=forms.PasswordInput
    )

    class Meta:
        """
        Meta class for UserSignupForm.

        Specifies the model and fields to be used in the form.
        """

        model = User
        fields = ("name", "phone", "email", "password", "password_confirmation")

    def clean(self):
        """
        Clean method for additional form-wide validation.

        Raises:
            forms.ValidationError: If the passwords do not match.
        Returns:
            dict: The cleaned form data.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("The passwords do not match.")

        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        """
        Save method to create and save a new user instance.

        Args:
            commit (bool): If True, save the user instance to the database.

        Returns:
            User: The created user instance.
        """
        user = super().save(commit=False)
        user.is_active = True
        user.role = RoleChoices.CUSTOMER
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class FarmerSignupForm(forms.ModelForm):
    """
    A form for farmer registration/signup.
    """

    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=156, required=True)
    phone = forms.CharField(max_length=20, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_confirmation = forms.CharField(
        label="Password Confirmation", widget=forms.PasswordInput
    )
    specialization = forms.ModelChoiceField(
        queryset=FarmProductCategory.objects.all(),
        widget=forms.Select(),
        required=True,
    )

    class Meta:
        """
        Meta class for FarmersSignupForm.

        Specifies the model and fields to be used in the form.
        """

        model = User
        fields = ("name", "phone", "email", "password", "password_confirmation")

    def clean(self):
        """
        Clean method for additional form-wide validation.

        Raises:
            forms.ValidationError: If the passwords do not match.
        Returns:
            dict: The cleaned form data.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("The passwords do not match.")

        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.role = RoleChoices.FARMER
        user.set_password(self.cleaned_data["password"])

        # Save the user before creating or getting the associated Farmer
        if commit:
            user.save()
            # Ensure user is saved before getting or creating Farmer
            farmer, created = Farmer.objects.get_or_create(user=user)

            if not created:
                # If Farmer already exists, update the specialization
                farmer.specialization = self.cleaned_data.get("specialization")
                farmer.save()
            else:
                # If Farmer is created, explicitly save it
                farmer.save()

        return user

    # @transaction.atomic
    # def save(self, commit=True):
    #     """
    #     Save method to create and save a new user instance and associated farmer.

    #     Args:
    #         commit (bool): If True, save the user instance to the database.

    #     Returns:
    #         User: The created user instance.
    #     """
    #     user = super().save(commit=False)
    #     user.is_active = True
    #     user.role = RoleChoices.FARMER
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()

    #     farmer, created = Farmer.objects.get_or_create(user=user)
    #     farmer.specialization = self.cleaned_data.get("specialization")
    #     farmer.save()

    #     return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "phone_no")


class FarmerProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(
        label="Bio",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Briefly describe yourself",
                "rows": "4",
                "cols": "25",
            },
        ),
    )

    class Meta:
        model = Farmer
        fields = (
            "specialization",
            "protect_email",
            "profile_image",
            "bio",
            "gender",
            "county",
            "town",
            "estate",
            "date_of_birth",
        )


class CustomerProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(
        label="Bio",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Briefly describe yourself",
                "rows": "4",
                "cols": "25",
            },
        ),
    )

    class Meta:
        model = Customer
        fields = (
            "bio",
            "gender",
            "profile_image",
            "county",
            "town",
            "estate",
            "date_of_birth",
        )
