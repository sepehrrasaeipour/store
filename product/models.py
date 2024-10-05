from django.utils.crypto import get_random_string
from django.db import models
import os
from django.contrib.auth.models import Permission, User
from django.core.validators import MaxValueValidator, MinValueValidator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    unique_id = get_random_string(length=15)
    final_name = f"image-{unique_id}{ext}"
    return f"products/{final_name}" # change directory name

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_num = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Product(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(default="", blank=True, null=True)
    price = models.IntegerField()
    discount = models.IntegerField(blank=True, null=True)
    sell_price = models.IntegerField(null=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_path)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField()
    is_sale = models.BooleanField(default=False)
    


    @property
    def discounted_price(self):
        return ((self.price)*(self.discount))/100

    @property
    def sell_price(self):
        return (self.price)-(self.discounted_price)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
