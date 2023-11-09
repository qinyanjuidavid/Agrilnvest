from unicodedata import category
from django import forms
from accounts.models import User, Administrator, Dealer, Customer,Counties
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db import transaction
from django.forms import ModelForm
from farmers.models import ProductCategory


class UserSignUpForm(ModelForm):
    email = forms.EmailField(max_length=156, required=True)
    phone = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ('username', "phone", 'email')

    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password don\'t match!')

        return password2

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user
class FarmerSignUpForm(ModelForm):
    email = forms.EmailField(max_length=156, required=True)
    phone = forms.CharField(max_length=20, required=True)
    category=forms.ModelChoiceField(
        queryset=ProductCategory.objects.all(),
        widget=forms.Select(),
        required=True
    )
    county=forms.ModelChoiceField(
        queryset=Counties.objects.all(),
        widget=forms.Select(),
        required=True
    )

    class Meta:
        model = User
        fields = ('username', "phone", 'email',"full_name")

    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password don\'t match!')

        return password2

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.role="Dealer"
        user.set_password(self.cleaned_data["password1"])
        user.save()
        if commit:
            user.save()
        dealerQs=Dealer.objects.create(user=user,
        category=self.cleaned_data.get('category'),
        county=self.cleaned_data.get("county")
        )
        return user

class FarmerProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(label="Bio",
                          widget=forms.Textarea(attrs={
                              "class": "form-control",
                              "placeholder": "Briefly describe yourself",
                              "rows": "4",
                              "cols": "25"
                          }))

    class Meta:
        model = Dealer
        fields = ("category", "protect_email",
                  "derivery", "response", "county",
                  "town", "estate", "profile_picture",
                  "bio",
                  )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("full_name", "phone",)


class CustomerProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(label="Bio",
                          widget=forms.Textarea(attrs={
                              "class": "form-control",
                                "placeholder": "Briefly describe yourself",
                              "rows": "4",
                              "cols": "25"
                          }))

    class Meta:
        model = Customer
        fields = ("bio", "profile_picture",
                  "county", "town", "estate")
