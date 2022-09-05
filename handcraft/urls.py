"""handcraft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from Application import views

urlpatterns = [
    path('', views.index, name="root"),
    path('product-detail/<str:id>', views.productDetails , name="product.detail"),
    path('add-cart/<str:id>', views.addCart , name="add.cart"),


    path('login', views.showLogin, name="login"),
    path('admin/home', views.home , name="admin.home"),
    path('admin_login', views.adminLogin, name="admin.login"),
    path('customer/logout', views.logout, name="logout"),

    path('admin/categories', views.showCategories, name="admin.category"),
    path('category/store', views.storeCategory, name="store.category"),
    path('category/update/<str:id>', views.updateCategory, name="update.category"),
    path('category/destroy/<str:id>', views.destroyCategory, name="destroy.category"),
    path('category/status/<str:id>/<str:status>', views.changeCategoryStatus, name="status.category"),

    path('customer/login', views.customerLogin, name="customer.login"),
    path('login/customer', views.loginCustomer, name="login.customer"),
    path('customer/signup', views.customerSignUp, name="customer.signup"),
    path('customer/store', views.storeCustomer, name="store.customer"),
    path('customer/add-cart/<str:id>' , views.addCart, name="add.cart"),

    path('shop/', views.shopList, name="shop.list"),
    path('blog/', views.blogList, name="blog.list"),
    path('contact-us/', views.contactUs, name="contact.us"),
    path('track-order/', views.trackOrder, name="track.order"),

    path('admin/products', views.showProducts, name="admin.products"),

    path('admin/customers', views.showCustomers, name="admin.customers"),

    path('admin/orders', views.showOrders, name="admin.orders"),

    path('admin/shipping', views.showShipping, name="admin.shipping"),

    path('admin/users', views.showUsers, name="admin.users"),

    path('admin/requests', views.showRequests, name="admin.requests"),

    path('admin/blogs', views.showBlogs, name="admin.blogs"),

    path('admin/contacts', views.showContacts, name="admin.contacts"),

    path('admin/subscribe', views.showSubscribe, name="admin.subscribe"),

    path('admin/site-info', views.showSiteInfo, name="admin.site.info"),

]
