from django.urls import path
from . import views

urlpatterns = [

    path("invoices/", views.invoice_list, name="invoice_list"),
    path("invoices/create/", views.create_invoice, name="create_invoice"),
    path("invoices/<int:pk>/", views.invoice_detail, name="invoice_detail"),

    path("payments/", views.payment_list, name="payment_list"),
    path("payments/create/", views.create_payment, name="create_payment"),
    path("payments/<int:pk>/", views.payment_detail, name="payment_detail"),

    path(
        "payments/<int:payment_id>/allocate/",
        views.allocate_payment_fifo,
        name="allocate_payment_fifo"
    ),

]
