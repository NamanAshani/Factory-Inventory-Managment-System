from django.db import models
from stock.models import Product
from order.models import Order


class Dispatch(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    dispatch_date=models.DateField(auto_now_add=True)
    vehicle_number=models.CharField(max_length=20)
    driver_name=models.CharField(max_length=100)
    total_weight=models.FloatField()
    delivery_type = models.CharField(max_length=50, choices=[
        ('full', 'FULL'),
        ('partial', 'PARTIAL'),
        
    ], default='full')
    status= models.CharField(max_length=50, choices=[
        ('in-transit', 'In-Transit'),
        ('delivered', 'Delivered'),
        
    ], default='in-transit')
    
    invoice_number = models.PositiveIntegerField(unique=True, null=True, blank=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Dispatch #{self.id} - Order #{self.order.ord_id} - {self.vehicle_number}"

    def save(self, *args, **kwargs):

        if not self.invoice_number:
            last_invoice = Dispatch.objects.order_by('-invoice_number').first()

            if last_invoice and last_invoice.invoice_number:
                self.invoice_number = last_invoice.invoice_number + 1
            else:
                self.invoice_number = 1

        super().save(*args, **kwargs)

class DispatchItem(models.Model):
    id = models.AutoField(primary_key=True)
    dispatch_id=models.ForeignKey(Dispatch,on_delete=models.CASCADE,null=True)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    pre_quantity = models.IntegerField(default=0) 
    std_quantity = models.IntegerField(default=0)
    com_quantity = models.IntegerField(default=0)
    eco_quantity = models.IntegerField(default=0)
    total_quantity = models.IntegerField(default=0)
    weight=models.FloatField()


    def save(self, *args, **kwargs):
        
        self.total_quantity = (
            self.pre_quantity +
            self.std_quantity +
            self.com_quantity +
            self.eco_quantity
        )
        super().save(*args, **kwargs)

    def __str__(self):
         return f"{self.product_id.pro_name}-{self.total_quantity}pcs(Dispatch #{self.dispatch_id})"