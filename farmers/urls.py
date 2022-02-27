from django.urls import path
from farmers import views

app_name = "farmers"

urlpatterns = [
    path("", views.homeView, name="home"),
    path("post/products/", views.productAddView, name="product_add"),
    path("dealers/detail/",
         views.dealersDetailsView, name="dealersDetails")
]
