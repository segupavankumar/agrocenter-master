from django.contrib.auth.models import AnonymousUser
from login.models import User
from django.shortcuts import render, redirect
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import FarmerRegisterForm
from django.contrib import messages
from .models import fruits, AandAdd
from shop.models import past_cart, past_items, order
import requests
import numpy as np
import re
from bs4 import BeautifulSoup
import json
from django.core.mail import send_mail,send_mass_mail
from backend.settings import EMAIL_HOST_USER
from background_task import background
from django.utils import timezone




def get_prices():
    f1 = open('vege.txt')
    a1 = f1.readlines()
    f2 = open('frui.txt')
    a2 = f2.readlines()
    result1 = []
    result2 = []
    for i in range(len(a1)):
        if(a1[i] != '\n' and a1[i] != 'Kg / Pcs\n'):
            result1.append(a1[i])

    for i in range(len(a2)):
        if(a2[i] != '\n' and a2[i] != 'Kg / Pcs\n'):
            result2.append(a2[i])
    fruits = []
    i = 5
    while(i < len(result1)):
        fruits.append(result1[i:i+4])
        i += 4
    j = 5
    while(j < len(result2)):
        fruits.append(result2[j:j+4])
        j += 4
    for i in fruits:
        u = len(i[0])
        i[0] = i[0][:u-1]
        x = len(i[1])
        i[1] = i[1][5:x-1]
        y = len(i[2])
        i[2] = i[2][5:y-1]
        z = len(i[3])
        i[3] = i[3][5:z-1]
    fruits = np.array(fruits)
    eq = '[0-9][0-9]*'
    range_of = []
    for i in fruits[:, 2]:
        range_of.append(re.findall(eq, i))

    fruit = zip(fruits[:, 0], range_of)
    return fruit


crop_names = []
crop_rates = []


def update_prices():
    crops = get_prices()
    for i in crops:
        crop_names.append(i[0])
        crop_rates.append(i[1])
update_prices()
def is_farmer(user):
    return user.is_farmer


def check(name):
    return name == ''


def user_fruits(user_id):
    frui = fruits.objects.filter(user_id=user_id)
    return frui


def check_amount(crop_name):
    index = crop_names.index(crop_name)
    min = int(crop_rates[index][0])*0.8
    min = round(min, 2)
    max = int(crop_rates[index][1])*1.2
    max = round(max, 2)

    list = [min, max]

    return list

# Create your views here.


@login_required
@user_passes_test(is_farmer, login_url='/user/login')
def add_details(request):
    
    if request.method == "POST":
        farmer_id = request.user.id
        crop = request.POST['crop']
        quantity = request.POST['quantity']
        amount = request.POST['amount']
        image = request.FILES['document']
        category = request.POST['category']

        a = check_amount(crop)
        if(int(amount) < int(a[0]) or int(amount) > int(a[1])):
            error = "enter amoiunt in range {} and {}"
            messages.error(request, error.format(a[0], a[1]))
            return redirect('add_details')

        if (check(crop) or check(category)):
            messages.error(request, "enter the correct inputs")
            return redirect('add_details')
        if image.size > 2621440:
            messages.error(
                request, "size of the image should be less than 2.5MB")
            return redirect('add_details')

        sold = User.objects.get(id=farmer_id)
        sold_by = sold.username
        id = fruits.objects.all().count()
        fruit = fruits(id=id, sold_by=sold_by, farmer_id=farmer_id, crop_name=crop,
                       category=category, quantity_in_kg=quantity,remaing_quantity= quantity, price_per_kg=amount, image=image)
        fruit.save()
        return redirect('/')
    else:
        id = fruits.objects.all().count()
        return render(request, 'farmer_add_crop.html', {'crop': crop_names, 'rates': crop_rates})


def farmer_signup(request):
    if request.method == 'POST':
        form = FarmerRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = FarmerRegisterForm()
    return render(request, 'signup.html', {'form': form})


@login_required()
def farmer_profile(request, name):
    try:
        farmer = User.objects.get(username=name)
    except User.DoesNotExist:
        farmer = None

    return render(request,'dashboard.html',{'user':farmer})


@user_passes_test(is_farmer, login_url='/user/login')
def farmer_edit_fruits(request):
    farmer_id = request.user.id
    fruit = fruits.objects.filter(farmer_id=farmer_id)
    return render(request, 'edit_orders.html', {'fruit': fruit})


@login_required()
def orders_(request):
    user = request.user
    id = request.user.id
    orders = order.objects.filter(user_id=id)

    cart_list = []
    amount = []
    for i in orders:
        amount.append(i.amount)
        cart_list.append(i.cart_id)

    past_carts = past_cart.objects.filter(id__in=cart_list)
    list_of_items = []
    quantity = []
    for i in past_carts:
        list_of_items.append(i.past_cart_list.all())

    ids = []
    lisof_crop = []
    rating = []
    for i in list_of_items:
        q = []
        l = []
        a = []
        t = []
        for j in i:
            q.append(fruits.objects.get(id=j.crop_id))
            l.append(j.quantity)
            a.append(j.rating)
            t.append(j.id)
        rating.append(a)
        ids.append(t)
        quantity.append(l)
        lisof_crop.append(q)

    items = []
    for i, j,z,v in zip(lisof_crop, quantity,rating,ids):
        lis = []
        for a in zip(i, j,z,v):
            lis.append(a)
        items.append(lis)

    fruit_ = zip(items, orders)

    return render(request, "orders_.html", {'fruit': fruit_, 'user': user})


@login_required()
def edit_fruits(request):
    data = json.loads(request.body)
    fruit_id = data['item_id']
    name = data['name']
    quantity = data['quantity']
    price = data['price']

    fruit = fruits.objects.get(id=fruit_id)
    fruit.crop_name = name
    fruit.quantity_in_kg = quantity
    fruit.price_per_kg = price

    fruit.save()
    return JsonResponse('done', safe=False)


@login_required()
def delete_fruit(request):
    data = json.loads(request.body)
    item_id = data['item_id']
    fruit = fruits.objects.get(id=item_id)
    fruit.suspend = True
    fruit.save()
    return JsonResponse("done", safe=False)

@login_required()
def profile(request):
    user = request.user
    try:
        obj = AandAdd.objects.get(id=user.id)
    except:
        obj = None
    if request.method == "POST":
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        phone = request.POST['number']
        address = request.POST['address']

        user.first_name = f_name
        user.last_name = l_name
        user.address = address
        user.phone_no = phone
        user.address = address
        user.save()

        if user.is_farmer:
            passbook = request.POST['passbook']
            account = request.POST['account']
            acc_type = request.POST['account type']
            ifsc = request.POST['ifcs']
            obj, created = AandAdd.objects.get_or_create(id=user.id)
            if(created == True):
                obj.account_no = account
                obj.passbook_no = passbook
                obj.account_type = acc_type
                obj.IFSC = ifsc
                subject = "verfivcation"
                messg = 'account verification is going on we will reach back to you'
                send_mail(subject,messg,EMAIL_HOST_USER,[request.user.email])
                obj.save()

        return redirect('/farmer/settings')

    return render(request, 'farmer_profile.html', {'user': user, 'obj': obj})


def revenue(request):
    user = request.user
    frui = fruits.objects.filter(farmer_id = user.id)
    return HttpResponse('<h1>Revenue</h1>')

def rating(request):
    data = json.loads(request.body)
    item_id = data['item_id']
    order_id = data['order_id']
    rating = data['rating']
    past_id = data['past_id']    
    orders = order.objects.get(id = order_id)
    past_item = past_cart.objects.get(id = orders.cart_id)
    item = past_item.past_cart_list.get(id = past_id)
    item.rating  = rating
    item.save()
    frui = fruits.objects.get(id = item_id)
    if frui.rating_count == None:
        frui.rating_count = 0
    if frui.total_rating == None:
        frui.total_rating = 0
    if frui.rating == None:
        frui.rating = 0
    frui.rating_count = frui.rating_count + 1
    frui.total_rating = frui.total_rating + rating
    frui.rating = int(frui.total_rating / frui.rating_count)
    frui.save()
    return JsonResponse('ok',safe=False)


