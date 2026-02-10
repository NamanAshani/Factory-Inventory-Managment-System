from django.db import models
from customer.models import Customer
from django.db.models import Sum

# new oreder
class Order(models.Model):
    ord_id = models.AutoField(primary_key=True) 
    pro_name = models.CharField(max_length=255)
    quan = models.IntegerField(default=0)
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
    pincode = models.IntegerField()
    ref_party = models.CharField(max_length=255)
    order_type = models.CharField(max_length=50)
    order_status = models.CharField(max_length=50)
    invioce_no = models.IntegerField()
    remark = models.CharField(max_length=255)
    mrp_zone = models.CharField(max_length=50)
    design = models.CharField(max_length=255)
    size = models.CharField(max_length=50)
    brand = models.CharField(max_length=255)
    punch_name  = models.CharField(max_length=255)
    pre_quantity = models.IntegerField(default=0) 
    std_quantity = models.IntegerField(default=0)
    com_quantity = models.IntegerField(default=0)
    eco_quantity = models.IntegerField(default=0)
    total_quentity = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.total_quentity = (
            self.pre_quantity +
            self.std_quantity +
            self.com_quantity +
            self.eco_quantity
        )
        super().save(*args, **kwargs)

        total = Order.objects.filter(
        cust_name=self.cust_name
        ).aggregate(
            Sum('total_quentity')
        )['total_quentity__sum'] or 0

        self.cust_name.cus_quantity = total
        self.cust_name.save()


    def delete(self, *args, **kwargs):

        customer = self.cust_name

        super().delete(*args, **kwargs)

        total = Order.objects.filter(
            cust_name=customer
        ).aggregate(
            Sum('total_quentity')
        )['total_quentity__sum'] or 0

        customer.cus_quantity = total
        customer.save()


    def __str__(self):
        return f"Order {self.ord_id}: {self.pro_name} ({self.quan}) - {self.status}"