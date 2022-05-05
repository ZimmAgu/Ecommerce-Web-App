# Create your models here.
from email.policy import default
from tkinter import CASCADE
from django.db import models
from django.conf import settings


class item (models.Model):                  # Stores individual items that can be ordered by a user
    name = models.CharField(max_length=50)  # Name of the item
    price = models.FloatField()             # Price of the item

    def __str__(self):
        return self.name                    # Items will be listed in the database using the item name


class orderItem (models.Model):                         # Once a user adds an item to the shopping cart, it becomes an order item
    item = models.ForeignKey(item,                      # item that belongs to a specific order
                            on_delete=models.CASCADE)


class order (models.Model):                             # Stores all of the items that the user has added to the cart
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  # User that the order belongs to
                            on_delete=models.CASCADE)  

    items = models.ManyToManyField(orderItem)           # Every order can have multiple items, and every item can be in multiple orders 
    dateAdded = models.DateTimeField(auto_now_add=True) # Moment that the order was created
    ordered = models.BooleanField(default=False)        # Whether or not the items in the shopping cart have been ordered
    dateOrdered = models.DateTimeField()                # Moment that the items in t

    def __str__(self):
        return self.user.username                       # Orders will be listed in the database using the username of the user that has made the order