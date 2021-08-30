from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import json
from django.db.models import Sum
from django.db.models import F
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from farmer.models import fruits
from .models import cart, cart_items, order,past_items,past_cart
from login.models import User
from django.template import Context
import re
import datetime
from django.utils.timezone import localtime
import pytz
import razorpay
from email.mime.text import MIMEText
from django.core.mail import send_mail,send_mass_mail
from backend.settings import EMAIL_HOST_USER

to_find = "[0-9][0-9][0-9]"
timeZ_Kl = pytz.timezone('Asia/Kolkata')

client = razorpay.Client(
        auth=("rzp_test_4bElxNBwAyNtYk", "S8npSCrqrSo4h9MhszNA1kfL"))

def days_after_upload():
    frui = fruits.objects.all()
    for i in frui:
        a = (datetime.datetime.now((timeZ_Kl)) - i.created_time).days


def avail_quantity(id):
    sum = fruits.objects.filter(crop_id=id).aggregate(Sum('quantity_in_kg'))


# shop
@login_required
def shop(request):
    '''

    *Functionality :*


    displays all the products initially

    *if the request method is post*

    three variabels are taken from the request object\n
    ``cat`` for category \n
    ``price`` for prce \n
    ``rating`` for the rating \n

    **Model**

    This view uses :model:`farmer.fruits`


    **Template**

    :template:`shop_home.html`



    '''
    l = []
    if 'crop' in request.POST:
        all_fruits = fruits.objects.filter(crop_name__icontains=request.POST['crop'])
    elif 'cat' in request.POST:
        all_fruits = fruits.objects.filter(category=request.POST['cat'])  & fruits.objects.filter(remaing_quantity__gt = 0)
    elif 'sort' in request.POST:
        all_fruits = fruits.objects.filter(rating__gte = request.POST['sort'][4])  & fruits.objects.filter(remaing_quantity__gt = 0)
    elif 'price' in request.POST:
        x = re.findall(to_find, request.POST['price'])
        if len(x) < 2:
            if request.POST['price'] == '<100':
                x.append(0)
            else:
                x.insert(0, 10000)
        all_fruits = fruits.objects.filter(
                    price_per_kg__lte=x[0]) & fruits.objects.filter(price_per_kg__gte=x[1]) & fruits.objects.filter(remaing_quantity__gt = 0)
    else:
        all_fruits = fruits.objects.filter(remaing_quantity__gt = 0)
    # days_after_upload()
    return render(request, 'shop_home.html', {'farfruits': all_fruits})


@login_required
def cart_(request):

    '''

    *Functionality :*

    displays all the products added to the cart

    **Model**

    This view uses :model:`shop.cart`


    **Template**

    :template:`cart.html`
   
    
    '''

    user_id = request.user.id
    try:
        cart_objects = cart.objects.get(user_id=user_id)
    except:
        return render(request, "cart.html", {'fruits': None})
    items = cart_objects.cart_list.filter(user_id__in=[user_id])
    list = []
    for i in items:
        list.append(i.crop_id)
    frui = fruits.objects.filter(id__in=list) & fruits.objects.filter(quantity_in_kg__gt = 0)
    Fruits = zip(frui, items)
    
    return render(request, "cart.html", {'fruits': Fruits})

@login_required
def checkout(request):
    '''

    *Functionality :*

    This view is intended to make series of calls to the razorpay api and creating the order object

    **Model**

    This view uses :model:`shop.cart` , :model:`farmer.fruits` , :model:`shop.order`


    **Template**

    :template:`test.html`
    
    '''

    user_id = request.user.id
    cart_objects = cart.objects.get(user_id=user_id)
    items = cart_objects.cart_list.filter(user_id__in=[user_id])
    list = []
    for i in items:
        list.append(i.crop_id)
    frui = fruits.objects.filter(id__in=list)
    Fruits = zip(frui, items)
    Order = order.objects.get(user=request.user,complete=False)
    amount = Order.amount/100

    response_ = client.order.create(dict(amount=Order.amount,currency = "INR",payment_capture='1'))
    order_id = response_['id']
    order_status = response_['status']
    context = Context()
    Order.transaction_id = order_id
    Order.save()

    if order_status == 'created':
        context['name'] = request.user.username
        try:
            context['phone'] = request.user.phone_no
            
        except:
            pass
        if request.user.address == 'no':
            Order.delete()
            return redirect('/farmer/settings')

            
        context['email'] = request.user.email
        context['order_id'] = order_id
    if request.method == "POST":
        Order.delete()
        return redirect('/shop')
    return render(request, "test.html", {'fruits': Fruits,'amount':amount,'context':context})




@login_required
@csrf_exempt
def payment_status(request):
    '''
    *Functionality :*

    this view is intended to capture the result of the payment and verify the payment and sending seriees of mails to both the user and the farmers

     **Model**

    This view uses :model:`shop.cart` , :model:`farmer.fruits` , :model:`shop.order`,:model:`shop.past_cart`


    **Template**

    :template:`order_summary.html`
    '''
    user_id = request.user.id
    res = request.POST
    params_dict = {
        'razorpay_order_id': res['razorpay_order_id'] ,
        'razorpay_payment_id': res['razorpay_payment_id'],
        'razorpay_signature': res[ 'razorpay_signature']
    }

    try:
        status = client.utility.verify_payment_signature(params_dict)
        Order = order.objects.get(transaction_id = res['razorpay_order_id']) 
        Order.complete = True
        Order.save()
        cart_objects = cart.objects.get(user_id=user_id)
        items = cart_objects.cart_list.filter(user_id__in=[user_id])
                            
        list = []
        for i in items:
            list.append(i.crop_id)
        l = past_cart.objects.all().count()
        Cart,created = past_cart.objects.get_or_create(id=l+1,user_id=user_id)
        frui = fruits.objects.filter(id__in=list)
        quan= []
        crop = []
        for i in items:
            quan.append(i.quantity)
            cartitem = past_items.objects.create(user_id=user_id, crop_id=i.crop_id,quantity = i.quantity)
            Cart.past_cart_list.add(cartitem)
            frui = fruits.objects.get(id = i.crop_id)
            crop.append(frui.crop_name)        
            frui.quantity_bought = frui.quantity_bought+i.quantity
            frui.amount = frui.amount +(i.quantity * frui.price_per_kg)
            frui.remaing_quantity = frui.remaing_quantity - i.quantity
            frui.save()

        user_ = []

        for i in range(len(list)):
            id_ = fruits.objects.get(id = list[i]).farmer_id
            user_.append(User.objects.get(id = id_).email)

        from_email = EMAIL_HOST_USER
        subject = 'Order recieved'
        message = 'A order has been recieved for  {}#crop name and the quantity is {} at the address {}'

        msg = []
        mail_list = []

        for i,j,k in zip(crop,quan,user_):
            m = message.format(i,j,request.user.address)
            mail_list.append((subject,m,from_email,[k]))
        send_mass_mail(tuple(mail_list),fail_silently=False)
                            
                
        Order.cart_id = Cart.id
        today = datetime.datetime.now().date()
        Order.deliverable_date =  today + datetime.timedelta(days=2) 
        Order.save()
        cart_objects.delete()
        items.delete()
                
        mesage_1 = "Greetings from Agrocentre \n Order placed succefully \n order id is {} \n Your product has been shipped from our end and you shall be receiving the product in the next 2-3 working days.\n Dispatch partner: Bluedart \n AWB Number: 69591278912 \n Transaction id is {}  "
        subject = "Order placed"
        msg = "\n https://bluedart.com/tracking"
        mesage_1 = mesage_1.format(Order.id,Order.transaction_id)  
        mesage_1 = mesage_1 + msg
        send_mail(subject,mesage_1,from_email,[request.user.email],fail_silently=False)
                        




        return render(request,'order_summary.html',{'status':'yes','order':Order})
    except :
        print(Exception)
        Order = order.objects.get(transaction_id = res['razorpay_order_id']).delete()
        return render(request,'order_summary.html',{'status':'no'})
        



def create_cart(request):
    data = json.loads(request.body)
    quantity = data['quantity']
    item_id = data['item_id']
    user_id = request.user.id
    cartitem, created = cart_items.objects.get_or_create(user_id=user_id, crop_id=item_id)
    Cart, created = cart.objects.get_or_create(id=user_id, user_id=user_id)
    car_ = Cart.cart_list.filter(
        user_id__in=[user_id]) & Cart.cart_list.filter(crop_id=item_id)
    for i in car_:
        return JsonResponse('item was added', safe=False)
    Cart.cart_list.add(cartitem)
    return JsonResponse('item was added', safe=False)


def remove_from_user_cart(request):
    data = json.loads(request.body)
    item_id = data['item_id']
    user_id = request.user.id
    cartitem = cart_items.objects.get(user_id=user_id, crop_id=item_id)
    Cart = cart.objects.get(id=user_id)
    Cart.cart_list.remove(cartitem)
    return JsonResponse('working', safe=False)


def update_cart(request):
    data = json.loads(request.body)
    quantity = data['quantities']
    ids = data['item_ids']

    user_id = request.user.id
    for i in range(len(ids)):
        ids[i] = int(ids[i])
        quantity[i] = int(quantity[i])
    
    for i in range(len(ids)):
        frui = fruits.objects.get(id = ids[i])
        if(quantity[i] > frui.quantity_in_kg):
            return JsonResponse('flop',safe=False)
    for i in range(len(ids)):
        cartitem = cart_items.objects.get(user_id=user_id, crop_id=ids[i])
        cartitem.quantity = quantity[i]
        cartitem.save()

    return JsonResponse('working', safe=False)


def order_creation(request):
    id = request.user.id
    cart_objects = cart.objects.get(user_id=id)
    items = cart_objects.cart_list.filter(user_id__in=[id])
    amount = 0
    data = json.loads(request.body)
    amount = data['amount']
    Order = order.objects.create(user=request.user, amount=amount*100)
    return JsonResponse('hi', safe=False)

