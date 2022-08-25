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
    category_id=models.ForeignKey("categories", on_delete=models.CASCADE)
    title=models.CharField(max_length=300)
    description=models.TextField()
    quantity=models.IntegerField()
    price=models.BigIntegerField()
    status=models.IntegerField(default=1)
    photo=models.ImageField(upload_to="uploads/products/")
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)
    
    
