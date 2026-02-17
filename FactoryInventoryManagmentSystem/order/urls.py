from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path("", views.order_home, name="order_home"),
=======
    path('', views.index, name='index'),
    # path("login/<str:role>/", views.login_view, name="login"),
   
>>>>>>> 837005349e0ed20cae26d1e38de198e46a5620b0
]
