# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from . models import Item, OrderItem, Order
from datetime import datetime

def homePage(request):
    context = { 'items' : Item.objects.all() }      # Assigns all items on the store to the variable name "items"
    return render(request, "homepage.html/", context)

def checkoutPage(request):
    return render(request, "checkoutPage.html/")

def productPage(request, slug):
    product = get_object_or_404(Item, slug=slug)    # Returns the item with the requested slug
    context = {'item' : product}                    # Assigns the returned produce the name "item"       
    return render(request, "productPage.html/", context)

def addToCart(request, slug):
    product = get_object_or_404(Item, slug=slug)        # Returns the item with the requested slug
    orderItem = OrderItem.objects.create(item=product)  # Adds an instance of the requested item to the OrderItem table
    orderQuerySet = Order.objects.filter(user=request.user, ordered=False)  # The items in the current user's shopping cart that have not been ordered

    if orderQuerySet.exists():      # If there are any items in the user's shopping cart that have been ordered
        order = orderQuerySet[0]    # Assigns the order found in the order query set to a variable

        if order.items.filter(product__slug=product.slug).exist():  # If the requested item is already in the cart
            orderItem.quantity += 1                                 # Increase the quantity of the ordered item by 1
            orderItem.save()                                        # Then save the changes made to the order item table
    else:                                                   # If  there are not any items in the user's shopping cart that have been ordered
        currentTime = datetime.now()
        order = Order.objects.create(user=request.user, dateOrdered=currentTime)     # Create a new order for the user
        order.items.add(orderItem)                          # Add the requested item to the newly requested order    

    response = redirect('coreFunctionality:productView', slug=slug)  # Once the item is added to the cart, the user is redirected back to the product page
    return response
