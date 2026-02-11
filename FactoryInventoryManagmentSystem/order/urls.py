from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='login'),
    # path("login/<str:role>/", views.login_view, name="login"),
   
]
