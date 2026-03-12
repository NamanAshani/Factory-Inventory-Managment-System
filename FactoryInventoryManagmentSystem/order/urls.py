from django.urls import path
from . import views

urlpatterns = [
    path("", views.order_home, name="order_home"),
    path("create/", views.order_create, name="order_create"),
    path("list/", views.order_list, name="order_list"),
    path("detail/<int:pk>/", views.order_detail, name="order_detail"),
    path("<int:pk>/update/", views.order_update, name="order_update"),
    path("<int:pk>/delete/", views.order_delete, name="order_delete"),
    path("magic/<int:product_id>/", views.order_magic, name="order_magic"),
    path("magic/<int:product_id>/update-allocation/", views.update_allocation, name="update_allocation"),
]
