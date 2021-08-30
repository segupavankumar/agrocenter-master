"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import path,include
from django.urls.conf import include
from django.conf.urls.static import  static
from django.conf import settings
from .views import home,about
from django.contrib.auth import views as auth
from django.contrib.sitemaps.views import sitemap


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('',home,name='home'),
    path('about/',about,name='about'),
    path('user/',include('login.urls')),
    path('shop/',include('shop.urls')),
    path('farmer/',include('farmer.urls')),
    path('doctor/',include('doctor.urls')),
    path('articles/',include('article.urls')),
    path('accounts',include('allauth.urls')),
    path('verification/', include('verify_email.urls')),	
    path('reset_password/',auth.PasswordResetView.as_view(), name='password_change'),
    path('reset_password_sent/',auth.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/',auth.PasswordResetCompleteView.as_view(), name='password_reset_complete')

]


urlpatterns = urlpatterns+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)