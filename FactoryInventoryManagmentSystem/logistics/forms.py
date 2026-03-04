from django import forms
from .models import Dispatch, DispatchItem
from order.models import Order
from stock.models import Product


class DispatchForm(forms.ModelForm):
    class Meta:
        model = Dispatch
        fields = [
            'order',
            'vehicle_number',
            'driver_name',
            'total_weight',
            'delivery_type',
            'status',
            'invoice_number'
        ]


class DispatchItemForm(forms.ModelForm):
    class Meta:
        model = DispatchItem
        fields = [
            'product_id',
            'pre_quantity',
            'std_quantity',
            'com_quantity',
            'eco_quantity'
        ]


class DispatchCreateForm(forms.Form):
    """Combined form for creating dispatch with items"""

    order = forms.ModelChoiceField(
        queryset=Order.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Order"
    )

    vehicle_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., MH 12 AB 1234'
        }),
        label="Vehicle Number"
    )

    driver_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Driver full name'
        }),
        label="Driver Name"
    )

    total_weight = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '0.00'
        }),
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
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'INV-2024-001'
        }),
        label="Invoice Number"
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter any additional notes...'
        }),
        label="Additional Notes"
    )