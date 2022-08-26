from django.shortcuts import render, redirect
from requests.sessions import session
from django.contrib import messages
from .models import *

# Website Methods
# Root of Application / 
def index(request):
    products = Product.objects.all()
    return render(request, 'website/index.html', {'products':products})

def productDetails(request , id):
    return render(request, 'website/product_details.html', {
        'product' : Product.objects.filter(id=id)
    })

def addCart(request , id):
    return null
    # product = Product.objects.filter(id=id)
    # Order(
    #     quantity= request.POST['quantity'],
    #     price= product.price * request.POST['quantity'],

    # )        

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
    return render(request, 'dashboard/product/product.html')

def showCustomers(request):
    return render(request, 'dashboard/customer/customer.html')

def showOrders(request):
    return render(request, 'dashboard/order/order.html')

def showShipping(request):
    return render(request, 'dashboard/shipping/shipping.html')

def showUsers(request):
    return render(request, 'dashboard/user/user_list.html')

def showRequests(request):
    return render(request, 'dashboard/request/request.html')

def showBlogs(request):
    return render(request, 'dashboard/website/blog.html')

def showContacts(request):
    return render(request, 'dashboard/website/contact.html')

def showSubscribe(request):
    return render(request, 'dashboard/website/subscribe.html')

def showSiteInfo(request):
    return render(request, 'dashboard/website/site_info.html')


