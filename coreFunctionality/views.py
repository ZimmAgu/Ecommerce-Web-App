# Create your views here.

# Django imports
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import ListView
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Folder imports
from . models import Item, OrderItem, Order
from .forms.forms import checkoutForm

# Miscellaneous imports
from datetime import datetime

class homePage(ListView):
    model = Item                        # Model that this view is based on
    template_name = "homepage.html"     # Template that this view is used to bring up
    paginate_by = 1                     # Amount of items that go on each page


class checkoutPage(View):
    model = Order
    def get(self, *args, **kwargs):
        form = checkoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False) 
        context = { 'form' : form, 'order' : order}
        return render(self.request, "checkoutPage.html/", context)


    def post(self, *args, **kwargs):
        form = checkoutForm(self.request.POST or None)
        print(self.request.POST)
        print("Errors Next")
        print(form.errors)
        if form.is_valid():
            print(form.cleaned_data)
            print("form works")
            return redirect('coreFunctionality:checkoutView')
        print("form didn't work")
        

def productPage(request, slug):
    product = get_object_or_404(Item, slug=slug)    # Returns the item with the requested slug
    context = {'item' : product}                    # Assigns the returned produce the name "item"       
    return render(request, "productPage.html/", context)



@login_required # Makes it a requirement for the user to be logged in to add anything to their cart
def addToCart(request, slug):
    product = get_object_or_404(Item, slug=slug)            # Returns the item with the requested slug

    orderItem, created = OrderItem.objects.get_or_create(   # Finds (or adds) an instance of the requested item to the OrderItem table
        item=product, 
        user=request.user, 
        ordered=False
    )  

    orderQuerySet = Order.objects.filter(user=request.user, ordered=False)  # The items in the current user's shopping cart that have not been ordered
    response = redirect('coreFunctionality:orderSummaryView')  


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



@login_required # Makes it a requirement for the user to be logged in to remove anything from their cart
def removeFromCart(request, slug):
    product = get_object_or_404(Item, slug=slug)            # Returns the item with the requested slug

    orderQuerySet = Order.objects.filter(user=request.user, ordered=False)  # The items in the current user's shopping cart that have not been ordered

    productViewResponse = redirect('coreFunctionality:productView', slug=slug)  # Once the item is added to the cart, the user is redirected back to the product page
    orderSummaryViwResponse = redirect('coreFunctionality:orderSummaryView')  


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
            return orderSummaryViwResponse             
        else:                   # If the requested item is not in the cart
            messages.info(request, "Item not in cart") 
            return productViewResponse      # Then there is nothing to remove to redirect the user back to the products page                       
    else:                                   # If there are no items in the user's cart
        messages.info(request, "You do not have an active order") 
        return productViewResponse          # Then there is nothing to remove to redirect the user back to the products page  



@login_required # Makes it a requirement for the user to be logged in to remove anything from their cart
def remove_Single_Cart_Item(request, slug):
    product = get_object_or_404(Item, slug=slug)            # Returns the item with the requested slug

    orderQuerySet = Order.objects.filter(user=request.user, ordered=False)  # The items in the current user's shopping cart that have not been ordered

    response = redirect('coreFunctionality:orderSummaryView')  # Once the item is added to the cart, the user is redirected back to the product page


    if orderQuerySet.exists():      # If there are any items in the user's shopping cart that have been ordered
        order = orderQuerySet[0]    # Assigns the order found in the order query set to a variable

        if order.items.filter(item__slug=product.slug).exists():    # If the requested item is already in the cart
            orderItem = OrderItem.objects.filter(                   # Finds an instance of the requested item to the OrderItem table
                item=product, 
                user=request.user, 
                ordered=False
            )[0]

            if orderItem.quantity > 1:      # (This if statement ensures the user will not be able to lower the quanitity lower than 1)
                orderItem.quantity -= 1     # lower the quanity by one
            orderItem.save()  
            messages.info(request, "Item quantity has been updated") 
            return response             
        else:                   # If the requested item is not in the cart
            messages.info(request, "Item not in cart") 
            return response     # Then there is nothing to remove to redirect the user back to the products page                       
    else:                       # If there are no items in the user's cart
        messages.info(request, "You do not have an active order") 
        return response         # Then there is nothing to remove to redirect the user back to the products page 



class orderSummary(LoginRequiredMixin,View):
    model = Order
    template_name = "orderSummary.html"
    

    def get(self, *args, **kwargs):
        try:                                                                    # If an order exists
            order = Order.objects.get(user=self.request.user, ordered=False)    #They get it
            context = {'order' : order}   
            return render(self.request, self.template_name, context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect('/')