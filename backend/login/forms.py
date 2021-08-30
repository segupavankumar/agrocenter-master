from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    number = forms.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ['username', 'email','number','password1', 'password2']