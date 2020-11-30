from django.shortcuts import render
from django.http import JsonResponse
import json
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
    # giving the same code as cart, bcz same, total data will be rendered in frontend
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
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.data)
    productId = data['productId']
    action = data['action']
    print('Action :', action)
    print('productId :',productId)
    return JsonResponse('Item was added', safe=False)
