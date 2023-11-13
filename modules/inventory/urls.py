from django.urls import path
from modules.inventory import views

app_name = "farmers"

urlpatterns = [
    path("", views.HomeView, name="home"),
]
