# Create your models here.
from email.policy import default
from django.db import models
from django.conf import settings
from django.urls import reverse

CATEGORIES = (  # Left value of each tuple element is what is deisplayed in the data base. Right value of each tuple element is what is displayed on screen
    ('S', 'Shirt'),
    ('SW', 'Sports Wear'),
    ('OW', 'Outwear'),
)

LABELCHOICES = (    # Color choices for the labels. Primary, secondary & danger 
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),    
)



class Item(models.Model):                  # Stores individual items that can be ordered by a user
    name = models.CharField(max_length=50)  # Name of the item
    price = models.FloatField()             # Price of the item
    category = models.CharField(max_length=2, choices=CATEGORIES, default='S')   # Category that the item is under
    label = models.CharField(max_length=1, choices=LABELCHOICES, default='P')    # Type of label that an item has (if it has one)
    slug = models.SlugField()
    description = models.TextField(default="This is a product")

    def __str__(self):
        return self.name                    # Items will be listed in the database using the item name

    def get_absolute_url(self):             # Retrieves the specific requested item got the product viewe page using the slug of the item
        return reverse('coreFunctionality:productView', kwargs={'slug' : self.slug})

    def get_Add_To_Cart_URL(self):
        return reverse('coreFunctionality:addToCartView', kwargs={'slug' : self.slug})
    
    def get_Remove_From_Cart_URL(self):
        return reverse('coreFunctionality:removeFromCartView', kwargs={'slug' : self.slug})



class OrderItem(models.Model):                                  # Once a user adds an item to the shopping cart, it becomes an order item
    user = models.ForeignKey(settings.AUTH_USER_MODEL,          # User that the order item belongs to
                            on_delete=models.CASCADE)  
    item = models.ForeignKey(Item, on_delete=models.CASCADE)    # item that belongs to a specific order
    quantity = models.IntegerField(default=1)                   # Amount of the item ordered
    ordered = models.BooleanField(default=False)                # Whether or not the specific item was ordered



    def __str__(self):
        return f"{self.quantity} of {self.item.name}"
    
    def get_total_price(self):
        return self.quantity * self.item.price


class Order(models.Model):                              # Stores all of the items that the user has added to the cart
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  # User that the order belongs to
                            on_delete=models.CASCADE)  

    items = models.ManyToManyField(OrderItem)           # Every order can have multiple items, and every item can be in multiple orders 
    dateAdded = models.DateTimeField(auto_now_add=True) # Moment that the order was created
    ordered = models.BooleanField(default=False)        # Whether or not the items in the shopping cart have been ordered
    dateOrdered = models.DateTimeField()                # Moment that the items in t

    def __str__(self):
        return self.user.username                       # Orders will be listed in the database using the username of the user that has made the order