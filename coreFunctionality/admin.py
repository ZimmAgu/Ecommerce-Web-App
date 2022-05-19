# Register your models here.
# Super user is Username: admin, Password: admin
from django.contrib import admin
from . models import Item, OrderItem, Order

admin.site.site_header = "Administration for Zim's Ecommerce Site"  # Changes the header of the adming page

admin.site.register(Item)       # Registers the item model on to the database
admin.site.register(OrderItem)  # Registers the orderItem model on to the database
admin.site.register(Order)      # Registers the order model on to the database
