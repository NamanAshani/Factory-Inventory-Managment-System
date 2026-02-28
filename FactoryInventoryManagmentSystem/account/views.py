from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice, Payment, PaymentAllocation
from django import forms
from django.contrib.auth.decorators import login_required

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["invoice_number", "customer", "order", "total_amount"]


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            "customer",
            "amount",
            "payment_date",
            "payment_mode",
            "reference_no",
            "remarks",
        ]

@login_required(login_url="login")
def invoice_list(request):

    invoices = Invoice.objects.all().order_by("-created_at")

    return render(
        request,
        "account/invoice_list.html",
        {"invoices": invoices}
    )


@login_required(login_url="login")
def create_invoice(request):

    form = InvoiceForm(request.POST or None)

    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.save()
        return redirect("invoice_list")

    return render(
        request,
        "account/create_invoice.html",
        {"form": form}
    )


@login_required(login_url="login")
def invoice_detail(request, pk):

    invoice = get_object_or_404(Invoice, id=pk)

    return render(
        request,
        "account/invoice_detail.html",
        {"invoice": invoice}
    )

@login_required(login_url="login")
def payment_list(request):

    payments = Payment.objects.all().order_by("-created_at")

    return render(
        request,
        "account/payment_list.html",
        {"payments": payments}
    )


@login_required(login_url="login")
def create_payment(request):

    form = PaymentForm(request.POST or None)

    if form.is_valid():
        payment = form.save(commit=False)
        payment.created_by = request.user
        payment.save()

        # 🔥 OPTIONAL: Auto FIFO allocation after saving
        allocate_fifo(payment)

        return redirect("payment_list")

    return render(
        request,
        "account/create_payment.html",
        {"form": form}
    )


@login_required(login_url="login")
def payment_detail(request, pk):

    payment = get_object_or_404(Payment, id=pk)

    return render(
        request,
        "account/payment_detail.html",
        {"payment": payment}
    )


def allocate_fifo(payment):

    remaining_amount = payment.amount

    # Get oldest unpaid invoices of this customer
    invoices = Invoice.objects.filter(
        customer=payment.customer
    ).exclude(status="paid").order_by("created_at")

    for invoice in invoices:

        if remaining_amount <= 0:
            break

        invoice_due = invoice.total_amount - invoice.paid_amount

        if invoice_due <= 0:
            continue

        # Amount to apply
        use_amount = min(invoice_due, remaining_amount)

        # Create allocation record
        PaymentAllocation.objects.create(
            payment=payment,
            invoice=invoice,
            amount_used=use_amount
        )

        # Update invoice
        invoice.paid_amount += use_amount

        if invoice.paid_amount >= invoice.total_amount:
            invoice.status = "paid"
        else:
            invoice.status = "partial"

        invoice.save()

        remaining_amount -= use_amount


@login_required(login_url="login")  
def allocate_payment_fifo(request, payment_id):

    payment = get_object_or_404(Payment, id=payment_id)

    allocate_fifo(payment)

    return redirect("payment_detail", pk=payment.id)
