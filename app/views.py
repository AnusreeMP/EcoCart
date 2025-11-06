from django.shortcuts import render,redirect
from .models import Product


# Create your views here.
def index(request):
    # items = Product.objects.all()[:8]
    items = []  # temporary placeholder
    return render(request, 'index.html', {'items': items})
 

def products(request):
    items = Product.objects.all()
    return render(request, 'products.html', {'items': items})



