from django.urls import path
from . import views

urlpatterns = [
    path('', views.itemList)  # Item list will be the homepage
]