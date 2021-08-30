from django import forms
from login.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class FarmerRegisterForm(UserCreationForm):
    email = forms.EmailField()
    number = forms.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ['username', 'email','number','password1', 'password2']
    
    def save(self, commit=True):
        User = super().save(commit=False)
        User.is_farmer = True
        if commit:
            User.save()
        return User