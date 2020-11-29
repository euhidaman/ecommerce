from django.shortcuts import render
from .models import  *

def store(request):
    products = Product.objects.all()
    context = {"products":products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # get_or_create is used to search for a qiven object,
        # and, if it isn't there, it then creates tht model object
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # the below line, is used to query from the OrderItem model
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

# Render cart data
