from django.urls import path
from . import views

urlpatterns = [
    path('', views.logistics_view, name='logistics_view'),
    path('add-dispatch/', views.add_dispatch, name='add_dispatch'),
    path('create-dispatch/', views.create_dispatch, name='create_dispatch'),
]