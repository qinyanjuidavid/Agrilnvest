from django import forms
# from farmers.models import Product
from accounts.models import Dealer, Product


class ProductAddForm(forms.ModelForm):
    description = forms.CharField(label="Description",
                                  widget=forms.Textarea(attrs={
                                      "class": "form-control",
                                      "placeholder": "Brief description of your product",
                                      "rows": "6",
                                      "cols": "25"
                                  }))
    quantity = forms.CharField(
        label="Quantity",
        widget=forms.TextInput(attrs={
            "placeholder": "Number of Kgs available"
        })
    )
    price = forms.CharField(
        label="Price",
        widget=forms.NumberInput(attrs={
            "placeholder": "Price per Kg"
        })
    )
    item = forms.CharField(
        label="Product",
        widget=forms.NumberInput(attrs={
            "placeholder": "Name of your farm product"
        })
    )

    class Meta:
        model = Product
        fields = ("item", "price", "quantity",
                  "description", "image")


class FarmerCategoryForm(forms.ModelForm):
    category = forms.CharField(disabled=True,
                               help_text="You can change the category in your profile. ",
                               widget=forms.TextInput(attrs={'readonly': True})
                               )

    class Meta:
        model = Dealer
        fields = ('category',)
