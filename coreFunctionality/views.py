# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . models import Item, OrderItem

def homePage(request):
    context = { 'items' : Item.objects.all() }      # Assigns all items on the store to the variable name "items"
    return render(request, "homepage.html/", context)

def checkoutPage(request):
    return render(request, "checkoutPage.html/")

def productPage(request, slug):
    product = get_object_or_404(Item, slug=slug)    # Returns the item with the requested slug
    context = {'item' : product}                    # Assigns the returned produce the name "item"       
    return render(request, "productPage.html/", context)

# def addToCart(request, slug):
#     item = get_object_or_404(item, slug=slug)       # Returns the item with the requested slug
#     order_Item = orderItem.objects.create(item=item)

