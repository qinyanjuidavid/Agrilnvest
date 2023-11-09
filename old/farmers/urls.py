from django.urls import path
from farmers import views

app_name = "farmers"

urlpatterns = [
    path("", views.homeView, name="home"),
    path("post/products/", views.productAddView, name="product_add"),
    path("farmer/<username>/details/",
         views.dealersDetailsView, name="dealersDetails"),
    path(
        "category/<str:category>/",
        views.CategoryFilterView, name="categoryFilter"
    ),
    path('farmer/rating', views.rateFarmer, name="rateFarmer"),
]
