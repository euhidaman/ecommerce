from django.shortcuts import render
from django.http import JsonResponse
import datetime
import json
from .models import  *

# remember to change the code here, to show total cart value at about page too
def about(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # get_or_create is used to search for a qiven object,
        # and, if it isn't there, it then creates tht model object
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # the below line, is used to query from the OrderItem model
        items = order.orderitem_set.all()
        # get_cart_items is a property of Order in models.py
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        # get_cart_items is a property of Order in models.py
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {"products":products, 'cartItems':cartItems}
    return render(request, 'store/about.html', context)

def store(request):
    # giving the same code as cart, bcz same, total data will be rendered in frontend
    if request.user.is_authenticated:
        customer = request.user.customer
        # get_or_create is used to search for a qiven object,
        # and, if it isn't there, it then creates tht model object
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # the below line, is used to query from the OrderItem model
        items = order.orderitem_set.all()
        # get_cart_items is a property of Order in models.py
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        # get_cart_items is a property of Order in models.py
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {"products":products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # get_or_create is used to search for a qiven object,
        # and, if it isn't there, it then creates tht model object
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # the below line, is used to query from the OrderItem model
        items = order.orderitem_set.all()
        # get_cart_items is a property of Order in models.py
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        # get_cart_items is a property of Order in models.py
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
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
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = ['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems, 'shipping':False}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action :', action)
    print('productId :',productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    # below line attaches the order to the given customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # in the below line, we r using 'get_or_create' to change the values of orderItem, if it already exists
    # so, if it already exists, we don't wan't to create orderItem again, we just want to change the quantity of orderItem
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action =='add':
        # by clicking up arrow, increment orderItem by 1
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        # by clicking up arrow, decrement orderItem by 1
        orderItem.quantity = (orderItem.quantity - 1)

    # save quantity of products, for an order
    orderItem.save()

    if orderItem.quantity <= 0:
        # remove the orderItem from cart, when quantity reaches 0, or below it
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
            )
    else:
        print("User is not logged in..")
    return JsonResponse("Payment submitted...",safe=False)
