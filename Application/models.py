from django.db import models

class User(models.Model):
    id=models.AutoField(primary_key=True)
    firstname=models.CharField(max_length=250)
    lastname=models.CharField(max_length=250)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=300)
    role=models.IntegerField(default=0)
    photo = models.ImageField(upload_to="uploads/user/")
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

class meta:
    db_table = 'users'

class Category(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=300)
    status=models.IntegerField(default=1)
    photo = models.ImageField(upload_to="uploads/category/")
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

class meta:
    db_table = 'categories'

class Product(models.Model):
    id=models.AutoField(primary_key=True)
    category=models.ForeignKey("Category", on_delete=models.CASCADE)
    title=models.CharField(max_length=300)
    description=models.TextField()
    quantity=models.IntegerField()
    price=models.BigIntegerField()
    status=models.IntegerField(default=1)
    photo=models.ImageField(upload_to="uploads/products/")
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

class meta:
    db_table = 'products'

class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    firstname=models.CharField(max_length=300)
    lastname=models.CharField(max_length=300)
    phone=models.CharField(max_length=30)
    email=models.CharField(max_length=300)
    username=models.CharField(max_length=300)
    password=models.CharField(max_length=300)
    photo=models.ImageField(upload_to="uploads/customers/")
    payment_type=models.IntegerField()
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)
    
class meta:
    db_table = 'customers'

class PaymentCard(models.Model):
    id=models.AutoField(primary_key=True)
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE)
    card_no=models.CharField(max_length=300)
    card_cvc=models.IntegerField()
    card_exp=models.CharField(max_length=300)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

class meta:
    db_table = 'payment_cards'

class Order(models.Model):
    id=models.AutoField(primary_key=True)
    product=models.ForeignKey('Product', on_delete=models.CASCADE)
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.BigIntegerField()
    order_status=models.IntegerField()
    shipping_zone=models.CharField(max_length=300)
    shipping_address=models.TextField()
    shipping_price=models.IntegerField()
    message=models.CharField(max_length=300)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)
    
class meta:
    db_table = 'orders'

class Refund(models.Model):
    id=models.AutoField(primary_key=True)
    order=models.ForeignKey('Order', on_delete=models.CASCADE)
    reason=models.TextField()
    refund_status=models.IntegerField()
    refund_message=models.CharField(max_length=300)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

class meta:
    db_table = 'refunds'

class TrackOrder(models.Model):
    id=models.AutoField(primary_key=True)
    order=models.ForeignKey('Order', on_delete=models.CASCADE)
    track_status=models.IntegerField()
    track_message=models.TextField()
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

class meta:
    db_table = 'track_orders'

class Blog(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=300)
    description=models.TextField()
    photo=models.ImageField(upload_to='uploads/blogs/')
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

class meta:
    db_table = 'blogs'

class Contact(models.Model):
    id=models.AutoField(primary_key=True)
    subject=models.CharField(max_length=300)
    email=models.CharField(max_length=300)
    message=models.TextField()
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

class meta:
    db_table = 'contacts'

class Subscribe(models.Model):
    id=models.AutoField(primary_key=True)
    email=models.CharField(max_length=300)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

class meta:
    db_table = 'subscribe'

class SiteInfo(models.Model):
    id=models.AutoField(primary_key=True)
    about_title=models.CharField(max_length=300)
    about_desc=models.TextField()
    email=models.CharField(max_length=300)
    phone=models.CharField(max_length=30)
    address=models.CharField(max_length=300)
    facebook=models.CharField(max_length=300)
    instagram=models.CharField(max_length=300)
    youtube=models.CharField(max_length=300)
    pinterest=models.CharField(max_length=300)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

class meta:
    db_table = 'site_info'

class WishList(models.Model):
    id=models.AutoField(primary_key=True)
    product=models.ForeignKey('Product', on_delete=models.DO_NOTHING)
    customer=models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

class meta:
    db_table = 'wishlist'

class RequestQuery(models.Model):
    id=models.AutoField(primary_key=True)
    subject=models.CharField(max_length=300)
    name=models.CharField(max_length=300)
    email=models.CharField(max_length=300)
    message=models.TextField()
    response=models.TextField()
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

class meta:
    db_table = 'requests'

class Shipping(models.Model):
    id = models.AutoField(primary_key=True)
    shipping_type = models.CharField(max_length=200)
    shipping_zone = models.CharField(max_length=200)
    price = models.BigIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class meta:
    db_table = 'shipping'













    
