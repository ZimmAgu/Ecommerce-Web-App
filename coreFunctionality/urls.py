from django.urls import path
from . import views

app_name="coreFunctionality"

urlpatterns = [
    path('', views.homePage),               # Item list will be the homepage
    path('checkout/', views.checkoutPage),  # Item list will be the homepage
    path('product/<slug:slug>/', views.productPage, name="productView")
]