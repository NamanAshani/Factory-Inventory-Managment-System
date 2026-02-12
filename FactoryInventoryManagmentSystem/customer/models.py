from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    customer_city = models.CharField(max_length=50)
    customer_date = models.DateTimeField(auto_now_add=True)
    cus_quantity = models.IntegerField(default=0)
    remark = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    truck_no = models.CharField(max_length=50)
    ref_party = models.CharField(max_length=255)


    def __str__(self):
        return self.customer_name