from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'product',
            'cust_name',
            'catagory',
            'country',
            'state',
            'city',
            'address',
            'pincode',
            'ref_party',
            'order_type',
            'order_status',
            'invoice_no',
            'remark',
            'mrp_zone',
            'size',
            'pre_quantity',
            'std_quantity',
            'com_quantity',
            'eco_quantity',
            'status',
        ]