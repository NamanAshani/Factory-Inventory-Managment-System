from django.urls import path
from . import views

urlpatterns = [

    path("add/", views.add_customer, name="add_customer"),
    path("list/", views.customer_list, name="customer_list"),
    path("<int:pk>/", views.customer_details, name="customer_details"),

]
