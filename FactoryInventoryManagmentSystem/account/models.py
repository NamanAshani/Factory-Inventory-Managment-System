from django.db import models, transaction
from django.db.models import F
from customer.models import Customer
from order.models import Order
from django.contrib.auth import get_user_model

User = get_user_model()

class Invoice(models.Model):

    STATUS_CHOICES = (
        ("unpaid", "Unpaid"),
        ("partial", "Partial"),
        ("paid", "Paid"),
    )

    invoice_number = models.CharField(max_length=50, unique=True)

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="invoices"
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="invoices"
    )

    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="unpaid"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number

    # 🔥 balance is CALCULATED — never save directly
    @property
    def balance_amount(self):
        return self.total_amount - self.paid_amount


class Payment(models.Model):

    PAYMENT_MODE = (
        ("cash", "Cash"),
        ("rtgs", "RTGS"),
        ("ach", "ACH"),
        ("neft", "NEFT"),
        ("swift", "SWIFT"),
        ("check", "Check"),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    payment_date = models.DateField()

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE
    )

    reference_no = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.customer}"

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        # FIRST SAVE PAYMENT
        super().save(*args, **kwargs)

        # Only run FIFO once (when created)
        if not is_new:
            return

        remaining_amount = self.amount

        invoices = Invoice.objects.filter(
            customer=self.customer,
            total_amount__gt=F("paid_amount")  # unpaid invoices
        ).order_by("created_at")

        with transaction.atomic():

            for invoice in invoices:

                if remaining_amount <= 0:
                    break

                # calculate balance
                balance = invoice.total_amount - invoice.paid_amount

                allocate_amount = min(balance, remaining_amount)

                PaymentAllocation.objects.create(
                    payment=self,
                    invoice=invoice,
                    amount_used=allocate_amount
                )

                # update paid_amount safely
                invoice.paid_amount += allocate_amount

                # update status properly
                if invoice.paid_amount == invoice.total_amount:
                    invoice.status = "paid"
                elif invoice.paid_amount > 0:
                    invoice.status = "partial"

                invoice.save()

                remaining_amount -= allocate_amount


class PaymentAllocation(models.Model):

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="allocations"
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="allocations"
    )

    amount_used = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment} → {self.invoice}"
