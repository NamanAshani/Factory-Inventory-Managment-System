from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path("login/<str:role>/", views.login_view, name="login"),
   
]

