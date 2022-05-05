# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from . models import item

def itemList (request):
    context = { 'items' : item.objects.all() }  # Assigns all items on the store to the variable name "items"
    return render(request, "itemList.html", context)


