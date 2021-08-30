from django.urls import path
from . import views
urlpatterns = [
    path('',views.articles,name = 'article'),
    path('<int:num>',views.page,name = 'pages')
]
