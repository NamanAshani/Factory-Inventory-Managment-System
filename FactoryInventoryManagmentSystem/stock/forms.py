from django import forms
from .models import Product, Stock


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['pro_name', 'design', 'brand', 'punch_name', 'remark']


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['product', 'pre_quantity', 'std_quantity', 'com_quantity', 'eco_quantity']