from django.shortcuts import render, redirect
from requests.sessions import session
from django.contrib import messages
from .models import *


def Customer_login_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if not (request.session.get('customer_id')):
            return redirect('customer.login')
        else:
            return function(request, *args, **kw)
    return wrapper

# Website Methods
# Root of Application / 
def index(request):
    if not (request.session.get('customer_id')):
        return render(request, 'website/index.html', {
            'products': Product.objects.all(),
            'categories': Category.objects.all(),
            'basketCount': 0,
            'wishlist' : 0,
        })
    else:
        cid = request.session.get('customer_id')
        return render(request, 'website/index.html', {
            'products': Product.objects.all(),
            'categories': Category.objects.all(),
            'basketCount': Order.objects.filter(customer_id=cid).count(),
            'wishlist' : WishList.objects.filter(customer_id=cid).count(),
            'orders': Order.objects.filter(customer_id=cid),
            'customer': Customer.objects.filter(id=cid),
        })

def productDetails(request , id):
    return render(request, 'website/product_details.html', {
        'product' : Product.objects.filter(id=id)
    })

def customerLogin(request):
    return render(request, 'website/login.html')

def loginCustomer(request):
    if request.method == "POST":
        username = request.POST['account_email']
        password = request.POST['account_password']

        if Customer.objects.filter(email=username).exists():
            user = Customer.objects.get(email=username)
            if user.password == password:
                request.session['customer_id'] = user.id
                request.session['customer_name'] = user.firstname
                return redirect('root')
            else:
                messages.error(request, "Incorrect Username or Password")
                return redirect('/')
        else:
            messages.error(request, "Incorrect Username or Password")
            return redirect('/')
       
def customerSignUp(request):
    return render(request, 'website/signup.html')

def storeCustomer(request):
    if request.method == "POST":
        result = Customer(
            firstname=request.POST['account_full_name'],
            email=request.POST['account_email'],
            password=request.POST['account_password'],
        )
        result.save()
        messages.success(request,"Account Registered Successfully")
        return redirect('customer.login')

@Customer_login_required
def addCart(request, id):
    product_id = id
    customer_id = request.session['customer_id']
    result = Order(
        quantity= 1, 
        price= 150,
        customer_id=customer_id,
        product_id=product_id,
    )
    result.save()
    messages.success(request,"Successfully")
    return redirect('root')

def shopList(request):
    return render(request, 'website/shop.html', {
        'products': Product.objects.all(),
        'categories': Category.objects.all(),
    })

def blogList(request):
    return render(request, 'website/blog.html', {
        'blogs': Blog.objects.all(),
        'categories': Category.objects.all(),
    })

def contactUs(request):
    return render(request, 'website/contactus.html')

def trackOrder(request):
    return render(request, 'website/track-order.html')


def logout(request):
    del request.session['customer_id']
    del request.session['customer_name']
    return redirect('root')
# Admin Panel Methods
# Login Page
def showLogin(request):
    return render(request, 'dashboard/user/login.html')

# ADMIN LOGIN
def adminLogin(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(email=username).exists():
            user = User.objects.get(email=username)
            if user.password == password:
                request.session['firstname'] = user.firstname
                request.session['lastname'] = user.lastname
                request.session['email'] = user.email
                request.session['photo'] = user.role
                messages.success(request, 'Welcome')
                return redirect('admin.home')
            else:
                messages.error(request, "Incorrect Username or Password")
                return redirect('/')
        else:
            messages.error(request, "Incorrect Username or Password")
            return redirect('/')
    else:
        messages.error(request, "Incorrect Username or Password")
        return redirect('/')

# HOME PAGE
def home(request):
    return render(request, 'dashboard/home/index.html')

# Show Category
def showCategories(request):
    category = Category.objects.all().order_by('-id')
    return render(request, 'dashboard/category/category.html', {'category': category})

# Add New Category
def storeCategory(request):
    if request.method == "POST":
        result = Category(
            name = request.POST['category'],
            photo = request.FILES['photo'],
        )
        result.save()
        messages.success(request,"Category Added Successfully")
        return redirect('admin.category')

def updateCategory(request , id):
    category = Category.objects.get(id=id)
    if request.method == "POST":
        if len(request.FILES) != 0:
            category.photo = request.FILES['photo']
        category.name = request.POST['category']
        category.save()
        messages.success(request,"Category Updated Successfully")
        return redirect('admin.category')


def destroyCategory(request , id):
    Category.objects.filter(id=id).delete()
    messages.success(request,"Category Deleted Successfully")
    return redirect('admin.category')

def changeCategoryStatus(request , id , status):
    Category.objects.filter(id=id).update(status=status)
    messages.success(request,"Category Status Changed")
    return redirect('admin.category')

def showProducts(request):
    return render(request, 'dashboard/product/product.html', {
        'products' : Product.objects.all().order_by('-id'),
        'categories' : Category.objects.all().order_by('-id')
    })

def storeProduct(request):
    if request.method == "POST":
        result = Product(
            title = request.POST['title'],
            description = request.POST['desc'],
            quantity = request.POST['quantity'],
            price = request.POST['price'],
            category_id = request.POST['category'],
            photo = request.FILES['photo'],
        )
        result.save()
        messages.success(request,"Product Published Successfully")
        return redirect('admin.products')

def updateProduct(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        if len(request.FILES) != 0:
            product.photo = request.FILES['photo']
        product.title = request.POST['title'],
        product.description = request.POST['desc'],
        product.quantity = int(request.POST['quantity']),
        product.price = int(request.POST['price']),
        product.save()
        messages.success(request,"Product Updated Successfully")
        return redirect('admin.products')


def showCustomers(request):
    return render(request, 'dashboard/customer/customer.html', {
        'customers' : Customer.objects.all().order_by('-id')
    })

def showOrders(request):
    return render(request, 'dashboard/order/order.html', {
        'orders' : Order.objects.all().order_by('-id')
    })

def showShipping(request):
    return render(request, 'dashboard/shipping/shipping.html')

def showUsers(request):
    return render(request, 'dashboard/user/user_list.html', {
        'users' : User.objects.all().order_by('-id')
    })

def showRequests(request):
    return render(request, 'dashboard/request/request.html')

def showBlogs(request):
    return render(request, 'dashboard/website/blog.html', {
        'blogs' : Blog.objects.all().order_by('-id')
    })

def showContacts(request):
    return render(request, 'dashboard/website/contact.html', {
        'contacts' : Contact.objects.all().order_by('-id')
    })

def showSubscribe(request):
    return render(request, 'dashboard/website/subscribe.html', {
        'subscribers' : Subscribe.objects.all().order_by('-id')
    })

def showSiteInfo(request):
    return render(request, 'dashboard/website/site_info.html', {
        'siteinfo' : SiteInfo.objects.first()
    })

# Website
