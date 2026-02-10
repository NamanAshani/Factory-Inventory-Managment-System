from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('login.html/', views.login, name='login'),
   
]
