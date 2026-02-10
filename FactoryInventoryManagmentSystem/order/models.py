from django.db import models
from customer.models import Customer

# new oreder
class Order(models.Model):
    ord_id = models.AutoField(primary_key=True) 
    pro_name = models.CharField(max_length=255)
    quan = models.IntegerField()
    ord_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled') 
    ], default='pending')
    cust_name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    catagory = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    pincode = models.IntegerField(max_length=6)
    ref_party = models.CharField(max_length=255)
    order_type = models.CharField(max_length=50)
    order_status = models.CharField(max_length=50)
    invioce_no = models.IntegerField(max_length=100)
    remark = models.CharField(max_length=255)
    mrp_zone = models.CharField(max_length=50)
    design = models.CharField(max_length=255)
    size = models.CharField(max_length=50)
    total_quentity = models.IntegerField()
    brand = models.CharField(max_length=255)
    punch_name  = models.CharField(max_length=255)
    pre_quantity = models.IntegerField() 
    std_quantity = models.IntegerField()
    com_quantity = models.IntegerField()
    eco_quantity = models.IntegerField()

    def __str__(self):
        return f"Order {self.ord_id}: {self.pro_name} ({self.quan}) - {self.status}"