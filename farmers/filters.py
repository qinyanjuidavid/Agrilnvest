from django.contrib.auth.models import User
from accounts.models import Dealer, User, Counties, ResponseTime
import django_filters
from django import forms
from farmers.models import ProductCategory


class OrderFilter(django_filters.FilterSet):
    query = ProductCategory.objects.all()
    locationQuery = Counties.objects.all().order_by("county")
    response_timeQuery = ResponseTime.objects.all()
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=query,
        widget=forms.CheckboxSelectMultiple,
        label=""
    )
    county = django_filters.ModelMultipleChoiceFilter(
        queryset=locationQuery,
        widget=forms.CheckboxSelectMultiple,
        label=""
    )
    response = county = django_filters.ModelMultipleChoiceFilter(
        queryset=response_timeQuery,
        widget=forms.CheckboxSelectMultiple,
        label=""
    )

    class Meta:
        model = Dealer
        fields = ("category", "county", "response")
