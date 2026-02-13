from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.home, name='login'),
    # path("login/<str:role>/", views.login_view, name="login"),
   
]
=======
    path('', views.index, name='index'),
]
>>>>>>> origin
