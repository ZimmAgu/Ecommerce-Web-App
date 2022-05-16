# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . models import item

def homePage(request):
    context = { 'items' : item.objects.all() }  # Assigns all items on the store to the variable name "items"
    return render(request, "homepage.html/", context)

def checkoutPage(request):
    return render(request, "checkoutPage.html/")

def productPage(request, slug):
    products = get_object_or_404(item, slug=slug)
    context = {'item' : products}
    return render(request, "productPage.html/", context)