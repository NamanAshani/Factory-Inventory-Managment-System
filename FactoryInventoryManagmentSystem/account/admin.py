from django.contrib import admin
from .models import Invoice, Payment, PaymentAllocation


admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(PaymentAllocation)
