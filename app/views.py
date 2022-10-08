from unicodedata import category
from django import dispatch
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from numpy import product
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from . models import Customer, Product, Cart, Orderplaced
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# home page
class home(View):
    def get(self, request):
        mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')
        camera = Product.objects.filter(category='C')
        headphones = Product.objects.filter(category='HE')
        return render(request, 'app/home.html', {'mobile': mobile, 'laptop': laptop, 'camera': camera, 'headphones': headphones})

# #product details


class ProductDetails(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = None
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})


@login_required
# cart add
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod-id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        # print(cart)
        amount = 0.0
        shipping_amount = 0.0
        total_amount = 0.0

        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                shipping_amount = 50.0
                total_amount = amount

            return render(request, 'app/addtocart.html', {'carts': cart, 'total': total_amount, 'amount': amount, 'shiping': shipping_amount})

        else:
            return render(request, 'app/emptycart.html')


@login_required
def plus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=user))
        c.quantity += 1
        c.save()

        amount = 0.0
        shiping_amount = 50

        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamt = (p.quantity * p.product.discounted_price)
                amount += tempamt

            data = {
                'amount': amount,
                'quantity': c.quantity,
                'totalamount': amount,
            }
            return JsonResponse(data)


@login_required
def minus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(user=user) & Q(product=prod_id))
        c.quantity -= 1
        c.save()

        amount = 0.0
        shiping_amount = 50

        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamt = (p.product.discounted_price * p.quantity)
                amount += tempamt

            data = {
                'amount': amount,
                'totalamount': amount,
                'quantity': c.quantity
            }
            return JsonResponse(data)


@login_required
def remove_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(user=user) & Q(product=prod_id))
        c.delete()

        amount = 0.0
        shiping_amount = 50

        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product == None:
            amount = 0.0
            shiping_amount = 0.0

        else:
            shiping_amount = 50
            for p in cart_product:
                tempamt = (p.product.discounted_price * p.quantity)
                amount += tempamt

            data = {
                'amount': amount,
                'totalamount': amount + shiping_amount,
            }
        return JsonResponse(data)

# Buy now


@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')


@method_decorator(login_required, name='dispatch')
class ProfileViews(View):
    def get(self, request):
        fm = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': fm, 'active': 'btn-primary'})

    def post(self, request):
        usr = request.user
        fm = CustomerProfileForm(request.POST)
        if fm.is_valid():
            name = fm.cleaned_data['name']
            locality = fm.cleaned_data['locality']
            state = fm.cleaned_data['state']
            city = fm.cleaned_data['city']
            zipcode = fm.cleaned_data['zipcode']
            user = Customer(user=usr, name=name, locality=locality,
                            state=state, city=city, zipcode=zipcode)
            user.save()
            messages.success(request, 'Your Profile Updated Successfully')
        return render(request, 'app/profile.html', {'form': fm, 'active': 'btn-primary'})

# address


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


@login_required
def orders(request):
    user = request.user
    op = Orderplaced.objects.filter(user=user)
    return render(request, 'app/orders.html', {'orders': op})


def mobile(request, data=None):
    if data == None:
        mobile = Product.objects.filter(category='M')
    elif data == 'Redme' or data == 'samsung':
        mobile = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobile = Product.objects.filter(
            category='M').filter(discounted_price__lt=20000)
    elif data == 'above':
        mobile = Product.objects.filter(
            category='M').filter(discounted_price__gt=20000)
    return render(request, 'app/mobile.html', {'mobiles': mobile})


def laptop(request, data=None):
    if data == None:
        laptop = Product.objects.filter(category='L')
    elif data == 'hp' or data == 'dell':
        laptop = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptop = Product.objects.filter(
            category='L').filter(discounted_price__lt=60000)
    elif data == 'above':
        laptop = Product.objects.filter(
            category='L').filter(discounted_price__gt=60000)
    return render(request, 'app/laptop.html', {'laptop': laptop})


def headphones(request, data=None):
    if data == None:
        hp = Product.objects.filter(category='HE')
    elif data == 'boat' or data == 'oneplus' or data == 'jbl':
        hp = Product.objects.filter(category='HE').filter(brand=data)
    elif data == 'below':
        hp = Product.objects.filter(category='HE').filter(
            discounted_price__lt=1000)
    elif data == 'above':
        hp = Product.objects.filter(category='HE').filter(
            discounted_price__gt=1000)
    return render(request, 'app/headphones.html', {'headphones': hp})


def camera(request, data=None):
    if data == None:
        cm = Product.objects.filter(category='C')
    elif data == 'nikon' or data == 'canon':
        cm = Product.objects.filter(category='C').filter(brand=data)
    elif data == 'below':
        cm = Product.objects.filter(category='C').filter(
            discounted_price__lt=40000)
    elif data == 'above':
        cm = Product.objects.filter(category='C').filter(
            discounted_price__gt=40000)
    return render(request, 'app/camera.html', {'camera': cm})


# Login form continue in urls.py


# password change view in url.py

class customerregistration(View):
    def get(self, request):
        fm = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': fm})

    def post(self, request):
        fm = CustomerRegistrationForm(data=request.POST)
        if fm.is_valid():
            # messages.success(request,'Congratulations !! Register Successfully')
            fm.save()
        return render(request, 'app/customerregistration.html', {'form': fm})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)

    amount = 0.0
    shiping_amount = 50
    totalamount = 0.0

    cart_product = [p for p in Cart.objects.all() if p.user == user]

    if cart_product:
        for p in cart_product:
            tempamt = (p.product.discounted_price * p.quantity)
            amount += tempamt
            totalamount = amount + shiping_amount
    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cartitems': cart_items})


@login_required
def paymentdone(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        Orderplaced(user=user, customer=customer,
                    product=c.product, quantity=c.quantity).save()
        c.delete()
        return redirect("orders")
