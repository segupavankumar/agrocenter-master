from django.urls import path,include
from . import views

urlpatterns = [
    path('crops',views.doctor_home,name = 'doctor home'),
    path('<str:plant_name>/part',views.part,name = 'part'),
    path('<str:plant_name>/<str:part>',views.disease,name = 'part'),
    path('<str:plant_name>/<str:part>/<str:disease>',views.info,name = 'info')
]
