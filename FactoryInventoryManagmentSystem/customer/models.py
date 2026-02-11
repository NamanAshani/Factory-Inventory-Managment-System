from django.db import models

# Create your models here.
class Customer(models.Model):
    Customer_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    Customer_city = models.CharField(max_length=50)
    Customer_date = models.DateTimeField(auto_now_add=True)
    customer_id = models.AutoField(primary_key=True)
    cus_quantity = models.IntegerField(default=0)
    mark = models.CharField(max_length=255)
    remark = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    truck_no = models.CharField(max_length=50)
    ref_party = models.CharField(max_length=255)


    def __str__(self):
        return self.Customer_name