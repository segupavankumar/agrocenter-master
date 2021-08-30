from django.contrib.auth.models import update_last_login
from django.db import models
from login.models import User
# Create your models here.

class fruits(models.Model):
    id = models.IntegerField(primary_key=True)
    sold_by = models.CharField(max_length=30)
    farmer_id = models.IntegerField(default = 0)
    crop_name = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    suspend = models.BooleanField(default=False)
    quantity_in_kg = models.IntegerField()
    quantity_bought = models.IntegerField(default=0)
    remaing_quantity = models.IntegerField(default = 0)
    rating = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    price_per_kg = models.IntegerField()
    image = models.ImageField(upload_to = 'images')
    amount = models.IntegerField(default=0)
    total_rating = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)


class AandAdd(models.Model):
    id = models.IntegerField(primary_key=True)
    account_id = models.CharField(max_length=20,blank=True)
    account_no = models.IntegerField(default=0)
    passbook_no = models.IntegerField(default=0)
    IFSC = models.CharField(max_length=15,null = True)
    account_type = models.CharField(max_length = 10,null=True)
    verified = models.BooleanField(default=False)

    