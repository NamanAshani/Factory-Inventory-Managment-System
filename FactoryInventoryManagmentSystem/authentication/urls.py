from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("ah_dashboard/", views.ah_dashboard, name="ah_dashboard"),
    path("dh_dashboard/", views.dh_dashboard, name="dh_dashboard"),
    path("mar_h_dashboard/", views.mar_h_dashboard, name="mar_h_dashboard"),
    path("md_dashboard/", views.md_dashboard, name="md_dashboard"),
    path("mh_dashboard/", views.mh_dashboard, name="mh_dashboard"),
    path("ph_dashboard/", views.ph_dashboard, name="ph_dashboard"),
]
