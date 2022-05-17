# Custom template tag to count the amount of items in a user cart
from django import template
from coreFunctionality.models import Order

register = template.Library()

@register.filter
def cartItemCount(user):
    if user.is_authenticated:   # If the user is autenticated
        querySet = Order.objects.filter(user=user, ordered=False)   # Make sure we are looking the the correct user's order, and that we are only looking at items they have not ordered yet
        
        if querySet.exists():                   # If the user does have items in their car
            return querySet[0].items.count()    # Return the amount of items they have
         
    return 0   # If the user isn't authenticated # Then return 0