import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except :
        cart = {}

    print('Cart: ',cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    # get_cart_items is a property of Order in models.py
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total']+=total
            order['get_cart_items']+=cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                    },
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems':cartItems, 'order':order, 'items':items}


def cartData(request):
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
        # cookieCart function is present in utils.py, and to use it, it's imported here
        # check utils.py for cookieCart function
        cookieData = cookieCart(request)
        # cookieData is a dictionary
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems, 'order':order, 'items':items}


def guestOrder(request, data):
    print("User is not logged in..")

    print("COOKIES:", request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created  = Customer.objects.get_or_create(
        email = email,
        )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete = False,
        )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
            )
    return customer, order
