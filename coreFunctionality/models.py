# Create your models here.
from email.policy import default
from django.db import models
from django.conf import settings

CATEGORIES = (  # Left value of each tuple element is what is deisplayed in the data base. Right value of each tuple element is what is displayed on screen
    ('S', 'Shirt'),
    ('SW', 'Sport Wear'),
    ('OW', 'Outwear'),
)

LABELCHOICES = (    # Color choices for the labels. Primary, secondary & danger 
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),    
)

class item (models.Model):                  # Stores individual items that can be ordered by a user
    name = models.CharField(max_length=50)  # Name of the item
    price = models.FloatField()             # Price of the item
    category = models.CharField(max_length=2, choices=CATEGORIES, default='S')   # Category that the item is under
    label = models.CharField(max_length=1, choices=LABELCHOICES, default='P')    # Type of label that an item has (if it has one)

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