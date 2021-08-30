from django.shortcuts import render
from .models import article
# Create your views here.

def articles(request):
    articles = article.objects.order_by('-pub_date')
    return render(request,'agro_news.html',{'articles':articles})

def page(request,num):
    articles = article.objects.get(id = num)
    return render(request,'article.html',{'article':articles})

