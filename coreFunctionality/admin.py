# Register your models here.
from django.contrib import admin
from .models import item, orderItem, order

admin.site.site_header = "Administration for Zim's Ecommerce Site"  # Changes the header of the adming page

admin.site.register(item)       # Registers the item model on to the database
admin.site.register(orderItem)  # Registers the orderItem model on to the database
admin.site.register(order)      # Registers the order model on to the database
