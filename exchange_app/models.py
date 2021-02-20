from django.db import models
from datetime import datetime
import re
import bcrypt


class UserManager(models.Manager):
    def user_validator(self, postdata):
        EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        errors = {}
        if len(postdata['first_name'])<1:
            errors['first_name']="You must provide a first name!"
        else:
            if len(postdata['first_name'])<2:
                errors['first_name']="First name should be more than 2 characters!"
        if len(postdata['last_name'])<1:
            errors['last_name']="You must provide a last name!"
        else:
            if len(postdata['last_name'])<2:
                errors['last_name']="Last name should be more than 2 characters!"
        if not EMAIL_REGEX.match(postdata['email']): 
            errors['email']="Email must be valid format!"
        if len(postdata['password'])<8:
            errors['password']="Password must be at least 8 characters!"
        if postdata['password'] != postdata['confirm_password']:
            errors['confirm_password']="Passwords do not match!"
        return errors

    def login_validator(self, postdata):
        errors = {}
        check = User.objects.filter(email=postdata['login_email'])
        if not check:
            errors['login_email'] = "Email has not been registered!"
        else:
            if not bcrypt.checkpw(postdata['login_password'].encode(), check[0].password.encode()):
                errors['login_email'] = "Email and password do not match!"
        return errors

class ItemManager(models.Manager):
    def item_validator(self, postdata):
        errors = {}
        if len(postdata['item_name'])<1:
            errors['item_name']="You must provide an item name!"
        if len(postdata['condition'])<1:
            errors['condition']="You must select a condition!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    condition = models.CharField(max_length=25)
    category = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    seller = models.ForeignKey(User, related_name="items", on_delete = models.CASCADE)
    buyer = models.ManyToManyField(User, related_name="item_buyer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=ItemManager()

# Create your models here.
