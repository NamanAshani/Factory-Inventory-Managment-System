from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("order/", include("order.urls")),
=======
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('order.urls')),
    path('stock/', include('stock.urls')),
>>>>>>> 837005349e0ed20cae26d1e38de198e46a5620b0
]

