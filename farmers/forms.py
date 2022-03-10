from django import forms
from farmers.models import Product


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
