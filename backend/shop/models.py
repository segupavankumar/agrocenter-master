from io import IncrementalNewlineDecoder
from django.db.models.fields import IntegerField
from django.db.models.query_utils import QueryWrapper
from farmer.models import fruits
from django.db import models
from django.db.models.base import Model
from login.models import User
from django.db.models.deletion import SET_NULL

# Create your models here.


class cart_items(models.Model):
    user_id = models.IntegerField(blank=True)
    crop_id = models.IntegerField(blank=True)
    quantity = models.IntegerField(null=True)


class cart(models.Model):
    cart_list = models.ManyToManyField(cart_items, blank=True)
    user_id = models.IntegerField(null=True)


class past_items(models.Model):
    user_id = models.IntegerField(blank=True)
    crop_id = models.IntegerField(blank=True)
    rating = models.IntegerField(default=0)
    quantity = models.IntegerField(null=True)

class past_cart(models.Model):
    id = models.IntegerField(primary_key=True)
    past_cart_list = models.ManyToManyField(past_items, blank=True)
    user_id = models.IntegerField(null=True)




class order(models.Model):
    cart_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    data_ordered = models.DateTimeField(auto_now_add=True)
    amount = IntegerField(blank=False)
    currency = models.CharField(default='INR', max_length=5)
    complete = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    deliverable_date = models.DateField(null = True)
    delivered_date = models.DateField(null=True)
    transaction_id = models.CharField(max_length=200)



