
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_farmer = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    address = models.CharField(default = 'no',max_length=300)
    phone_no = models.IntegerField(default=0)


class mailinglist(models.Model):
    email = models.EmailField()
