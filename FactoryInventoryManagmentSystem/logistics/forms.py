from django import forms
from .models import Dispatch, DispatchItem
from order.models import Order
from stock.models import Product

class DispatchForm(forms.ModelForm):
    class Meta:
        model = Dispatch
        fields = ['order', 'vehicle_number', 'driver_name', 'total_weight', 
                 'delivery_type', 'status', 'invoice_number']
        widgets = {
            'order': forms.Select(attrs={'class': 'form-control'}),
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., MH 12 AB 1234'}),
            'driver_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Driver full name'}),
            'total_weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'delivery_type': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('full', 'FULL'),
                ('partial', 'PARTIAL'),
            ]),
            'status': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('in-transit', 'In-Transit'),
                ('delivered', 'Delivered'),
            ]),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'INV-2024-001'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show orders that haven been fully dispatched or are pending
        self.fields['order'].queryset = Order.objects.all().order_by('-ord_id')
        self.fields['order'].label_from_instance = lambda obj: f"Order #{obj.ord_id} - {obj.cust_name}"


class DispatchItemForm(forms.ModelForm):
    class Meta:
        model = DispatchItem
        fields = ['product_id', 'pre_quantity', 'std_quantity', 'com_quantity', 
                 'eco_quantity', 'total_quantity', 'weight']
        widgets = {
            'product_id': forms.Select(attrs={'class': 'form-control'}),
            'pre_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'std_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'com_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'eco_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'total_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'readonly': 'readonly'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_id'].queryset = Product.objects.all().order_by('pro_name')
        self.fields['product_id'].label_from_instance = lambda obj: obj.pro_name


class DispatchCreateForm(forms.Form):
    """Combined form for creating dispatch with items"""
    order = forms.ModelChoiceField(
        queryset=Order.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Order"
    )
    vehicle_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., MH 12 AB 1234'}),
        label="Vehicle Number"
    )
    driver_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Driver full name'}),
        label="Driver Name"
    )
    total_weight = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        label="Total Weight (kg)"
    )
    delivery_type = forms.ChoiceField(
        choices=[('full', 'FULL'), ('partial', 'PARTIAL')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Delivery Type"
    )
    status = forms.ChoiceField(
        choices=[('in-transit', 'In-Transit'), ('delivered', 'Delivered')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status",
        initial='in-transit'
    )
    invoice_number = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'INV-2024-001'}),
        label="Invoice Number"
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter any additional notes...'}),
        label="Additional Notes"
    )