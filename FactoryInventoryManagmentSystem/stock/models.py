from django.db import models
from django.db.models import Sum

class Product(models.Model):
    pro_id = models.AutoField(primary_key=True)
    pro_name = models.CharField(max_length=255)
    design = models.CharField(max_length=255)
    # size = models.CharField(max_length=50)
    brand = models.CharField(max_length=255)
    punch_name  = models.CharField(max_length=255)
    remark = models.CharField(max_length=255)

    def __str__(self):
        return self.pro_name

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    pre_quantity = models.IntegerField(default=0) 
    std_quantity = models.IntegerField(default=0)
    com_quantity = models.IntegerField(default=0)
    eco_quantity = models.IntegerField(default=0)
    total_quantity = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        
        self.total_quantity = (
            self.pre_quantity +
            self.std_quantity +
            self.com_quantity +
            self.eco_quantity
        )

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


    def __str__(self):
        if self.product:
            return f"{self.product.pro_name} - {self.total_quantity}"
        return "No Product"