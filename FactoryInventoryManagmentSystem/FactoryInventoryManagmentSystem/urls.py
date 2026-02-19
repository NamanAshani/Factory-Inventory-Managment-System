from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('authentication.urls')),
    path("order/", include("order.urls")),
    path("stock/", include("stock.urls")),
    path("login/", include("authentication.urls")),
    path("account/", include("account.urls")),
    path("customers/", include("customer.urls")),
]

