from django import forms
from farmers.models import Product
from accounts.models import Farmer


class ProductAddForm(forms.ModelForm):
    description = forms.CharField(label="Description",
                                  widget=forms.Textarea(attrs={
                                      "class": "form-control",
                                      "placeholder": "Brief description about the product",
                                      "rows": "6",
                                      "cols": "25"
                                  }))

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
        model = Farmer
        fields = ('category',)
