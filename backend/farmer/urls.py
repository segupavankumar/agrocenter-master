from django import urls
from django.urls import path
from . import views

urlpatterns = [
path('add_details',views.add_details,name= 'add_details'),
path('signup',views.farmer_signup,name='signup'),
path('f/<str:name>',views.farmer_profile,name='profile'),
path('all_products',views.farmer_edit_fruits,name='edit_fruits'),
path('edit_fruit',views.edit_fruits,name="edit"),
path('delete_fruit',views.delete_fruit,name="delete"),
path('order',views.orders_,name="orders"),
path('settings',views.profile,name='pr'),
path('revenue',views.revenue,name='rev'),
path('rating',views.rating,name='rating')

]