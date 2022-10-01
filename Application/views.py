from django.shortcuts import render, redirect
from requests.sessions import session
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection
import json
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
    NewProductsList = Product.objects.all().reverse()[:8]
    PopularProductList = Product.objects.all()[:10]
    category = Category.objects.all()


    if not (request.session.get('customer_id')):
        return render(request, 'website/index.html', {
            'products': NewProductsList ,
            'popular' : PopularProductList,
            'categories': category,
        })
    else:
        cid = request.session.get('customer_id')
        basketCount = Order.objects.filter(customer_id=cid).count()
        wishlist = WishList.objects.filter(customer_id=cid).count()
        return render(request, 'website/index.html', {
            'products': NewProductsList,
            'popular' : PopularProductList,
            'categories': category,
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
                request.session['customer_photo'] = json.dumps(str(user.photo))
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
        quantity= request.POST['quantity'], 
        price= request.POST['price'],
        customer_id=customer_id,
        product_id=product_id,
        order_status=0,
    )
    result.save()
    messages.success(request,"Successfully Added to cart")
    return redirect(request.META.get('HTTP_REFERER'))

def shopList(request):
    return render(request, 'website/shop.html', {
        'products': Product.objects.all(),
        'categories': Category.objects.all(),
    })

def blogList(request):
    return render(request, 'website/blog.html', {
        'blogs': Blog.objects.all(),
    })

def getSingleBlog(request , id):
    return render(request, 'website/single_blog.html', {
        'blog': Blog.objects.filter(id=id).first()
    })

def contactUs(request):
    return render(request, 'website/contactus.html', {
        'siteInfo' : SiteInfo.objects.filter(id=1).first()
    })

def storeContact(request):
    if request.method == "POST":
        Contact(
            subject= request.POST['subject'],
            email= request.POST['email'],
            message = request.POST['message']
        ).save()
        messages.success(request,"You Messaged US Successfully")
        return redirect(request.META.get('HTTP_REFERER'))

def aboutUs(request):
     return render(request, 'website/about.html', {
        'siteInfo' : SiteInfo.objects.filter(id=1).first()
    })

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
    jan_order = Order.objects.filter(created__month=1).count()
    feb_order = Order.objects.filter(created__month=2).count()
    mar_order = Order.objects.filter(created__month=3).count()
    apr_order = Order.objects.filter(created__month=4).count()
    may_order = Order.objects.filter(created__month=5).count()
    jun_order = Order.objects.filter(created__month=6).count()
    jul_order = Order.objects.filter(created__month=7).count()
    aug_order = Order.objects.filter(created__month=8).count()
    sep_order = Order.objects.filter(created__month=9).count()
    oct_order = Order.objects.filter(created__month=10).count()
    nov_order = Order.objects.filter(created__month=11).count()
    dec_order = Order.objects.filter(created__month=12).count()

    jan_cust = Customer.objects.filter(created__month=1).count()
    feb_cust = Customer.objects.filter(created__month=2).count()
    mar_cust = Customer.objects.filter(created__month=3).count()
    apr_cust = Customer.objects.filter(created__month=4).count()
    may_cust = Customer.objects.filter(created__month=5).count()
    jun_cust = Customer.objects.filter(created__month=6).count()
    jul_cust = Customer.objects.filter(created__month=7).count()
    aug_cust = Customer.objects.filter(created__month=8).count()
    sep_cust = Customer.objects.filter(created__month=9).count()
    oct_cust = Customer.objects.filter(created__month=10).count()
    nov_cust = Customer.objects.filter(created__month=11).count()
    dec_cust = Customer.objects.filter(created__month=12).count()
    return render(request, 'dashboard/home/index.html', {
        'orders' : Order.objects.count(),
        'customers' : Customer.objects.count(),
        'products' : Product.objects.count(),
        'subscribers' : Subscribe.objects.count(),
        'jan_order' : jan_order, 'feb_order': feb_order , 'mar_order': mar_order,
        'apr_order' : apr_order, 'may_order': may_order , 'jun_order': jun_order,
        'jul_order' : jul_order, 'aug_order': aug_order , 'sep_order': sep_order,
        'oct_order' : oct_order, 'nov_order': nov_order , 'dec_order': dec_order,
        'jan_cust' : jan_cust, 'feb_cust': feb_cust , 'mar_cust': mar_cust,
        'apr_cust' : apr_cust, 'may_cust': may_cust , 'jun_cust': jun_cust,
        'jul_cust' : jul_cust, 'aug_cust': aug_cust , 'sep_cust': sep_cust,
        'oct_cust' : oct_cust, 'nov_cust': nov_cust , 'dec_cust': dec_cust,
    })

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
        'products' : Product.objects.raw("SELECT * FROM application_product INNER JOIN 	application_category ON application_product.category_id = application_category.id"),
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
        product.category_id = request.POST['category']
        product.title = request.POST['title']
        product.description = request.POST['desc']
        product.quantity = int(request.POST['quantity'])
        product.price = int(request.POST['price'])
        product.save()
        messages.success(request,"Product Updated Successfully")
        return redirect('admin.products')

def destroyProduct(request, id):
    Product.objects.filter(id=id).delete()
    messages.success(request,"Product Deleted Successfully")
    return redirect('admin.products')

def changeProductStatus(request , id , status):
    Product.objects.filter(id=id).update(status=status)
    messages.success(request,"Product Status Changed")
    return redirect('admin.products')

def showCustomers(request):
    return render(request, 'dashboard/customer/customer.html', {
        'customers' : Customer.objects.all().order_by('-id')
    })

def customerDestroy(request , id):
    Customer.objects.filter(id=id).delete()
    messages.success(request,"Customer Deleted Successfully")
    return redirect('admin.customers')

def showOrders(request):
    return render(request, 'dashboard/order/order.html', {
        'orders' : Order.objects.raw("SELECT * FROM application_customer INNER JOIN application_order on application_customer.id = application_order.customer_id INNER JOIN application_product ON application_product.id = application_order.product_id;")
    })

def showTracking(request , id):
    return render(request, 'dashboard/order/tracking.html', {
        'tracks' : TrackOrder.objects.filter(order_id=id),
        'order_id': id
    })

def storeTrack(request , id):
    if request.method == "POST":
        TrackOrder(
            order_id = id,
            track_status= request.POST['track_status'],
            track_message= request.POST['track_message'],
        ).save()
        messages.success(request,"Track Status Added Successfully")
        return redirect('/track/order/'+id)

def updateTrack(request , id):
    track = TrackOrder.objects.get(id=id)
    if request.method == "POST":
        track.track_status = request.POST['track_status']
        track.track_message = request.POST['track_message']
        track.save()
        
        messages.success(request,"Track Status Updated Successfully")
        return redirect(request.META.get('HTTP_REFERER'))

def destroyTrack(request , id):
    TrackOrder.objects.filter(id=id).delete()
    messages.success(request,"Track Status Deleted Successfully")
    return redirect('admin.orders')

def showShipping(request):
    return render(request, 'dashboard/shipping/shipping.html', {
        'shipping' : Shipping.objects.all().order_by('-id')
    })

def storeShipping(request):
    if request.method == "POST":
        Shipping(
            shipping_type= request.POST['shipping_type'],
            shipping_zone= request.POST['shipping_zone'],
            price= request.POST['price']
        ).save()
        messages.success(request,"New Shipping Added Successfully")
        return redirect('admin.shipping')

def updateShipping(request, id):
    shipping = Shipping.objects.get(id=id)
    if request.method == "POST":
        shipping.shipping_type = request.POST['shipping_type']
        shipping.shipping_zone = request.POST['shipping_zone']
        shipping.price  = request.POST['price']
        shipping.save()
        messages.success(request,"Shipping Updated Successfully")
        return redirect('admin.shipping')


def showUsers(request):
    return render(request, 'dashboard/user/user_list.html', {
        'users' : User.objects.all().order_by('-id')
    })

def storeUser(request):
    if request.method == "POST":
        user = User(
            firstname= request.POST['firstname'],
            lastname= request.POST['lastname'],
            email= request.POST['email'],
            role= request.POST['role'],
            password= request.POST['password'],
            photo= request.FILES['photo'],
        )
        user.save()
        messages.success(request,"User Added Successfully")
        return redirect('admin.users')

def updateUser(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        if len(request.FILES) != 0:
            user.photo = request.FILES['photo']
        user.firstname = request.POST['firstname']
        user.lastname = request.POST['lastname']
        user.email = request.POST['email']
        user.role = request.POST['role']
        user.password = request.POST['password']
        user.save()
        messages.success(request,"User Updated Successfully")
        return redirect('admin.users')

def destroyUser(request , id):
    user = User.objects.filter(id=id).delete()
    if(user):
        messages.success(request,"User Deleted Successfully")
        return redirect('admin.users')

def showRequests(request):
    return render(request, 'dashboard/request/request.html', {
        'requests' : RequestQuery.objects.all().order_by('-id')
    })

def replyRequest(request, id):
    requests = RequestQuery.objects.get(id=id)
    if request.method == 'POST':
        requests.response = request.POST['response']
        requests.save()
        messages.success(request,"Response Added Successfully")
        return redirect('admin.requests')

def destroyRequest(request, id):
    requests = RequestQuery.objects.filter(id=id).delete()
    if(requests):
        messages.success(request,"Request Deleted Successfully")
        return redirect('admin.requests')

# Blogs
def showBlogs(request):
    return render(request, 'dashboard/website/blog.html', {
        'blogs' : Blog.objects.all().order_by('-id')
    })

def storeBlog(request):
    if request.method == "POST":
        blog = Blog(
            title= request.POST['title'],
            description= request.POST['desc'],
            photo= request.FILES['photo']
        )
        blog.save()
        messages.success(request,"Post Published Successfully")
        return redirect('admin.blogs')

def updateBlog(request, id):
    blog = Blog.objects.get(id=id)
    if request.method == "POST":
        if len(request.FILES) != 0:
            blog.photo = request.FILES['photo']
        blog.title = request.POST['title']
        blog.description = request.POST['desc']
        blog.save()
        messages.success(request,"Post Updated Successfully")
        return redirect('admin.blogs')
    

def destroyBlog(request , id):
    blog = Blog.objects.filter(id=id).delete()
    if(blog):
        messages.success(request,"Post Deleted Successfully")
        return redirect('admin.blogs')

def showContacts(request):
    return render(request, 'dashboard/website/contact.html', {
        'contacts' : Contact.objects.all().order_by('-id')
    })

def destroyContact(request , id):
    contact = Contact.objects.filter(id=id).delete()
    if(contact):
        messages.success(request,"Contacts Deleted Successfully")
        return redirect('admin.contacts')

def showSubscribe(request):
    return render(request, 'dashboard/website/subscribe.html', {
        'subscribers' : Subscribe.objects.all().order_by('-id')
    })

def showSiteInfo(request):
    return render(request, 'dashboard/website/site_info.html', {
        'siteinfo' : SiteInfo.objects.first()
    })

def updateSiteInfo(request , id):
    site = SiteInfo.objects.get(id=id)
    if request.method == "POST":
        site.about_title = request.POST['title']
        site.about_desc = request.POST['desc']
        site.email = request.POST['email']
        site.phone = request.POST['phone']
        site.address = request.POST['address']
        site.facebook = request.POST['facebook']
        site.instagram = request.POST['instagram']
        site.youtube = request.POST['youtube']
        site.pinterest = request.POST['pinterest']
        site.save()
        messages.success(request,"Site Information Updated Successfully")
        return redirect('admin.site.info')

def subscribe(request):
    if request.method == "POST":
        Subscribe(
            email= request.POST['subscriber_email'],
        ).save()

        messages.success(request,"You Subscribed Successfully")
        return redirect(request.META.get('HTTP_REFERER'))

@Customer_login_required
def getCartPage(request):
    cid = request.session.get('customer_id')
    cart = Order.objects.raw("SELECT application_product.title,  application_product.description , application_product.photo , application_order.id , application_order.quantity , application_order.price , application_order.order_status , (application_order.quantity * application_order.price) as total_price , application_order.customer_id  FROM application_product INNER JOIN application_order ON application_product.id = application_order.product_id WHERE order_status = 0 AND application_order.customer_id ="+str(cid))
    orders = Order.objects.raw("SELECT * , SUM(price * quantity) as total FROM application_order WHERE customer_id = 1 AND order_status = 0")
    return render(request, 'website/card.html', {
        'cart' : cart,
        'orders' : orders,
    })

def removeCart(request, id):
    Order.objects.filter(id=id).delete()
    messages.success(request,"You Removed Form Cart Successfully")
    return redirect(request.META.get('HTTP_REFERER'))

def checkout(request , total):
    cid = request.session.get('customer_id')
    shipping = Shipping.objects.all()
    customer = Customer.objects.filter(id=cid).first()
    return render(request, 'website/checkout.html', {
        'total' : total,
        'shipping' : shipping,
        'customer' : customer
    })

def placeOrder(request):
    cid = request.session.get('customer_id')
    if request.method == "POST":
        cursor = connection.cursor()
        cursor.execute("UPDATE application_order SET order_status = 1, shipping_zone = '"+request.POST['shipping_zone']+"' , shipping_address='"+request.POST['ship_address']+"'  WHERE order_status = 0 AND customer_id = "+str(cid))
        cust = Customer.objects.get(id=cid)
        cust.firstname = request.POST['firstname']
        cust.lastname = request.POST['lastname']
        cust.phone = request.POST['phone']
        cust.save()

        if request.POST['card_no'] != "":
            PaymentCard(
                customer_id = cid ,
                card_no= request.POST['card_no'],
                card_cvc= request.POST['cvc'],
                card_exp= request.POST['expire_date']
            ).save()

        messages.success(request,"Your Order Submited Successfully")
        return redirect('root')

@Customer_login_required
def myAccount(request):
    cid = request.session.get('customer_id')
    return render(request, 'website/myaccount.html', {
        'account': Customer.objects.filter(id=cid).first()
    })

def UpdateAccount(request, id):
    cust = Customer.objects.get(id=id)
    if request.method == "POST":
        if len(request.FILES) != 0:
            cust.photo = request.FILES['photo']
        if request.POST['password'] == "":
            cust.password = request.POST['password']

        cust.firstname = request.POST['firstname']
        cust.lastname = request.POST['lastname']
        cust.phone = request.POST['phone']
        cust.email = request.POST['email']
        cust.save()
        messages.success(request,"Your Account Update Successfully")
        return redirect(request.META.get('HTTP_REFERER'))

def addWishlist(request , id):
    cid = request.session.get('customer_id')
    WishList(
        customer_id = cid , 
        product_id = id 
    ).save()
    messages.success(request,"Your Account Update Successfully")
    return redirect(request.META.get('HTTP_REFERER'))


@Customer_login_required
def myWishlist(request):
    cid = request.session.get('customer_id')
    return render(request, 'website/wishlist.html', {
        'wishlist' : Product.objects.raw("SELECT * ,application_wishlist.id as wid  FROM application_product INNER JOIN application_wishlist ON application_product.id=application_wishlist.product_id WHERE customer_id="+str(cid))
    })

def removeWishlist(request , id):
    WishList.objects.filter(id=id).delete()
    messages.success(request,"Product Removed From Wishlist Successfully")
    return redirect(request.META.get('HTTP_REFERER'))

@Customer_login_required
def myOrders(request):
    cid = request.session.get('customer_id')
    cart = Order.objects.raw("SELECT application_product.title,  application_product.description , application_product.photo , application_order.id , application_order.quantity , application_order.price , application_order.order_status , (application_order.quantity * application_order.price) as total_price , application_order.customer_id  FROM application_product INNER JOIN application_order ON application_product.id = application_order.product_id WHERE order_status = 1 AND application_order.customer_id ="+str(cid))
    return render(request, 'website/myorders.html', {
        'cart' : cart
    })

def trackMyOrder(request, id):
    tracks = TrackOrder.objects.filter(order_id=id)
    return  render(request, 'website/trackorder.html', {
        'tracks' : tracks,
        'order_id' : id,
    })    

def refundOrder(request , id):
    refund = Refund.objects.filter(order_id=id)
    return  render(request, 'website/refund.html', {
        'refund' : refund,
        'order_id' : id,
    })    

def sendRefundOrder(request , id):
    if request.method == "POST":
        Refund(
            refund_status= 1, 
            refund_message= request.POST['message'],
            order_id = id
        ).save()
        messages.success(request,"Refund Request Send Successfully")
        return redirect(request.META.get('HTTP_REFERER'))


@Customer_login_required
def accountSetting(request):
    cid = request.session.get('customer_id')
    payments = PaymentCard.objects.filter(customer_id=cid).first()
    return render(request, 'website/account_setting.html', {
        'payment' : payments,
    })

def updateCard(request , id):
    paymentCard = PaymentCard.objects.get(id=id)
    if request.method == "POST":
        paymentCard.card_no = request.POST['card_no']
        paymentCard.card_cvc = request.POST['cvc']
        paymentCard.card_exp = request.POST['card_exp']
        paymentCard.save()
        messages.success(request,"Card Payments Updated Successfully")
        return redirect(request.META.get('HTTP_REFERER'))

def searchData(request):
    search = request.GET['data']
    products = Product.objects.filter(title__icontains=search) | Product.objects.filter(description__icontains=search)
    return render(request, 'website/search.html', {
        'products' : products,
        'search' : search
    })


def searchCategory(request, id):
    return render(request, 'website/shop.html', {
        'products' : Product.objects.filter(category_id=id),
        'categories' : Category.objects.all(),
    })

def AdminLogout(request):
    del request.session['firstname']
    del request.session['lastname']
    del request.session['email']
    del request.session['photo']
    return redirect('login')


def getInfo(request):
    siteInfo = SiteInfo.objects.filter(id=1).first()
    title = siteInfo.about_title
    desc = siteInfo.about_desc
    email = siteInfo.email
    phone = siteInfo.phone
    address = siteInfo.address
    facebook = siteInfo.facebook
    instagram = siteInfo.instagram
    youtube = siteInfo.youtube
    pinterest = siteInfo.pinterest
     
    if not (request.session.get('customer_id')):
        return JsonResponse({
            'basketCount': 0,
            'wishlist' : 0,
            'customer' : 0,
            'title' : title , 
            'desc' : desc,
            'email' : email,
            'phone' : phone,
            'address' : address,
            'facebook' : facebook,
            'instagram' : instagram,
            'youtube' : youtube,
            'pinterest' : pinterest,
        })
    else:
        cid = request.session.get('customer_id')
        basketCount = Order.objects.raw("SELECT * , COUNT(id) as bsk FROM application_order WHERE order_status = 0 AND customer_id = "+str(cid))
        wishlist = WishList.objects.filter(customer_id=cid).count()
        customer = Customer.objects.filter(id=cid).first()
        return JsonResponse({
            'basketCount': basketCount[0].bsk,
            'wishlist' : wishlist,
            'customer' : customer.firstname+" "+customer.lastname,
            'title' : title , 
            'desc' : desc,
            'email' : email,
            'phone' : phone,
            'address' : address,
            'facebook' : facebook,
            'instagram' : instagram,
            'youtube' : youtube,
            'pinterest' : pinterest,
        })
# Website
