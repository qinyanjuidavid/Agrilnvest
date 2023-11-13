from django.contrib.auth.models import User
import django_filters
from django import forms

from modules.accounts.models import FarmProductCategory, Farmer


class FarmerFilter(django_filters.FilterSet):
    query = FarmProductCategory.objects.all()
    # locationQuery = Counties.objects.all().order_by("county")
    # response_timeQuery = ResponseTime.objects.all()
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=query,
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": ""},
        ),
        label="",
    )
    # county = django_filters.ModelMultipleChoiceFilter(
    #     queryset=locationQuery,
    #     widget=forms.CheckboxSelectMultiple,
    #     label=""
    # )
    # response = django_filters.ModelMultipleChoiceFilter(
    #     queryset=response_timeQuery,
    #     widget=forms.CheckboxSelectMultiple,
    #     label=""
    # )

    class Meta:
        model = Farmer
        fields = ("category",)
