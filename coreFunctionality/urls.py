from django.urls import path
from . import views

app_name="coreFunctionality"

urlpatterns = [
    path('', views.itemList),  # Item list will be the homepage
    path('checkout/', views.checkoutPage)  # Item list will be the homepage
]