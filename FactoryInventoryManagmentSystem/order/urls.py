from django.urls import path
from . import views

urlpatterns = [
     path("", views.order_home, name="order_home"),
    path("create/", views.order_create, name="order_create"),
    path("<int:pk>/update/", views.order_update, name="order_update"),
]
