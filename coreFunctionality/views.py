# Create your views here.

# Django imports
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import ListView
from django.core.paginator import Paginator

# Model imports
from . models import Item, OrderItem, Order

# Miscellaneous imports
from datetime import datetime

class homePageListView(ListView):
    model = Item                        # Model that this view is based on
    template_name = "homepage.html"     # Template that this view is used to bring up
    paginate_by = 1                     # Amount of items that go on each page


def checkoutPage(request):
    return render(request, "checkoutPage.html/")


def productPage(request, slug):
    product = get_object_or_404(Item, slug=slug)    # Returns the item with the requested slug
    context = {'item' : product}                    # Assigns the returned produce the name "item"       
    return render(request, "productPage.html/", context)


def addToCart(request, slug):
    product = get_object_or_404(Item, slug=slug)            # Returns the item with the requested slug

    orderItem, created = OrderItem.objects.get_or_create(   # Finds (or adds) an instance of the requested item to the OrderItem table
        item=product, 
        user=request.user, 
        ordered=False
    )  

    orderQuerySet = Order.objects.filter(user=request.user, ordered=False)  # The items in the current user's shopping cart that have not been ordered
    response = redirect('coreFunctionality:productView', slug=slug)  


    if orderQuerySet.exists():      # If there are any items in the user's shopping cart that have been ordered
        order = orderQuerySet[0]    # Assigns the order found in the order query set to a variable

        if order.items.filter(item__slug=product.slug).exists():    # If the requested item is already in the cart
            orderItem.quantity += 1                                 # Increase the quantity of the ordered item by 1
            orderItem.save()                                        # Then save the changes made to the order item table
            messages.success(request, "Item quantity updated")
            return response
        else:                                                       # If the requested item is not in the cart
            order.items.add(orderItem)                              # Then add it to the cart
            messages.success(request, "Item added to cart")
            return response
    else:                                                   # If  there are not any items in the user's shopping cart that have been ordered
        currentTime = datetime.now()
        order = Order.objects.create(user=request.user, dateOrdered=currentTime)     # Create a new order for the user
        order.items.add(orderItem)                          # Add the requested item to the newly requested order   
        messages.success(request, "Item added to cart") 
        return response




def removeFromCart(request, slug):
    product = get_object_or_404(Item, slug=slug)            # Returns the item with the requested slug

    orderQuerySet = Order.objects.filter(user=request.user, ordered=False)  # The items in the current user's shopping cart that have not been ordered

    response = redirect('coreFunctionality:productView', slug=slug)  # Once the item is added to the cart, the user is redirected back to the product page


    if orderQuerySet.exists():      # If there are any items in the user's shopping cart that have been ordered
        order = orderQuerySet[0]    # Assigns the order found in the order query set to a variable

        if order.items.filter(item__slug=product.slug).exists():    # If the requested item is already in the cart
            orderItem = OrderItem.objects.filter(                   # Finds an instance of the requested item to the OrderItem table
                item=product, 
                user=request.user, 
                ordered=False
            )[0]

            order.items.remove(orderItem)                           # Then remove it from the cart
            messages.info(request, "Item removed from cart") 
            return response             
        else:                   # If the requested item is not in the cart
            messages.info(request, "Item not in cart") 
            return response     # Then there is nothing to remove to redirect the user back to the products page                       
    else:                       # If there are no items in the user's cart
        messages.info(request, "Order does not exist") 
        return response         # Then there is nothing to remove to redirect the user back to the products page   