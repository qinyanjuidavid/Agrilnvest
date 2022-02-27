from django.urls import path
from farmers import views

app_name = "farmers"

urlpatterns = [
    path("home/", views.homeView, name="home"),
    path("", views.welcomeView, name="welcome"),
    path("post/products/", views.productAddView, name="product_add"),
]
