from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("order_home/", views.order_home, name="order_home"),
]
