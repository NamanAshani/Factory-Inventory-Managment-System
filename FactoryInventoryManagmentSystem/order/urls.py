from django.urls import path
from . import views

urlpatterns = [
    path("", views.order_home, name="order_home"),
    path("list/", views.order_list, name="order_list"),
    path("<int:pk>/", views.order_details, name="order_details"),
]
