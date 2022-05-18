from django.urls import path
from . import views

app_name="coreFunctionality"

urlpatterns = [
    path('', views.homePage.as_view()),               # Item list will be the homepage
    path('checkout/', views.checkoutPage, name="checkoutView"),  # Item list will be the homepage
    path('product/<slug:slug>/', views.productPage, name="productView"),
    path('add-to-cart/<slug:slug>/', views.addToCart, name="addToCartView"),
    path('remove-from-cart/<slug:slug>/', views.removeFromCart, name="removeFromCartView"),
    path('remove-single-item-from-cart/<slug:slug>/', views.remove_Single_Cart_Item, name="remove-Single-Item-From-Cart-View"),
    path('order-summary/', views.orderSummary.as_view(), name="orderSummaryView"),
]