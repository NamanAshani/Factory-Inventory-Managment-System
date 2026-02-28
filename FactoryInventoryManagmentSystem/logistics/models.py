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
    invoice_number=models.CharField(max_length=500)

    def __str__(self):
        return f"Dispatch #{self.id} - Order #{self.order.ord_id} - {self.vehicle_number}"


class DispatchItem(models.Model):
    id = models.AutoField(primary_key=True)
    dispatch_id=models.ForeignKey(Dispatch,on_delete=models.CASCADE,null=True)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    product_type=models.CharField(max_length=9)
    quantity=models.IntegerField()
    weight=models.FloatField()

    def __str__(self):
         return f"{self.product_id.pro_name}-{self.quantity}pcs(Dispatch #{self.dispatch_id})"