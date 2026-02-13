from django.contrib import admin
<<<<<<< HEAD
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('order.urls')),
]
=======
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('order/', include('order.urls')),
]
>>>>>>> origin
