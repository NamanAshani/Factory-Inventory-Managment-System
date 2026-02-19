from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("ph_dashboard/", views.ph_dashboard, name="ph_dashboard")

]
