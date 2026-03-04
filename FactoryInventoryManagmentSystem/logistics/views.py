from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Dispatch, DispatchItem
from stock.models import Product
from order.models import Order
from django.contrib.auth.decorators import login_required
from .forms import DispatchForm, DispatchItemForm
from django.shortcuts import get_object_or_404
from django.db.models import Count

@login_required(login_url="login")
def logistics_view(request):

    # Get all dispatch items with related data
    dispatch_items = DispatchItem.objects.select_related('dispatch_id', 'product_id').all().order_by('-dispatch_id__dispatch_date')
    
    # Filter variables
    product_name = ""
    vehicle_number = ""
    driver_name = ""
    delivery_type = ""
    status = ""
    invoice_number = ""
    type_filter = ""
    min_range = ""
    max_range = ""

    if request.method == "GET":
        
        # Get filter values from GET parameters
        product_name = request.GET.get('product_name', '')
        vehicle_number = request.GET.get('vehicle_number', '')
        driver_name = request.GET.get('driver_name', '')
        delivery_type = request.GET.get('delivery_type', '')
        status = request.GET.get('status', '')
        invoice_number = request.GET.get('invoice_number', '')
        type_filter = request.GET.get('type', '')
        min_range = request.GET.get('min_range', '')
        max_range = request.GET.get('max_range', '')

        # Apply product name filter
        if product_name:
            dispatch_items = dispatch_items.filter(
                product_id__pro_name__icontains=product_name
            )

        # Apply vehicle number filter
        if vehicle_number:
            dispatch_items = dispatch_items.filter(
                dispatch_id__vehicle_number__icontains=vehicle_number
            )

        # Apply driver name filter
        if driver_name:
            dispatch_items = dispatch_items.filter(
                dispatch_id__driver_name__icontains=driver_name
            )

        # Apply delivery type filter
        if delivery_type:
            dispatch_items = dispatch_items.filter(
                dispatch_id__delivery_type=delivery_type
            )

        # Apply status filter
        if status:
            dispatch_items = dispatch_items.filter(
                dispatch_id__status=status
            )

        # Apply invoice number filter
        if invoice_number:
            dispatch_items = dispatch_items.filter(
                dispatch_id__invoice_number__icontains=invoice_number
            )

        # Field mapping for type filter (PRE/STD/ECO/COM dropdown)
        field_map = {
            "pre": "pre_quantity",
            "std": "std_quantity",
            "eco": "eco_quantity",
            "com": "com_quantity",
            "total": "total_quantity",
        }

        # Apply type filter with range
        if type_filter in field_map:
            field = field_map[type_filter]
            filters = {}

            try:
                min_val = int(min_range) if min_range else None
                max_val = int(max_range) if max_range else None

                # Swap if min > max (same logic as stock view)
                if min_val is not None and max_val is not None:
                    if min_val > max_val:
                        min_val, max_val = max_val, min_val

                if min_val is not None:
                    filters[f"{field}__gte"] = min_val

                if max_val is not None:
                    filters[f"{field}__lte"] = max_val

                if filters:
                    dispatch_items = dispatch_items.filter(**filters)

            except ValueError:
                pass  # Ignore if values are not integers

    # Calculate totals for footer
    total_pre = sum(item.pre_quantity for item in dispatch_items)
    total_std = sum(item.std_quantity for item in dispatch_items)
    total_eco = sum(item.eco_quantity for item in dispatch_items)
    total_com = sum(item.com_quantity for item in dispatch_items)
    total_all = sum(item.total_quantity for item in dispatch_items)

    # Get unique values for filter dropdowns
    products = Product.objects.all().order_by('pro_name')
    vehicles = Dispatch.objects.values_list('vehicle_number', flat=True).distinct().order_by('vehicle_number')
    drivers = Dispatch.objects.values_list('driver_name', flat=True).distinct().order_by('driver_name')
    invoices = Dispatch.objects.values_list('invoice_number', flat=True).distinct().order_by('invoice_number')
    
    # Get orders for dispatch creation modal
    orders = Order.objects.all().order_by('-ord_id')

    context = {
        "dispatch_items": dispatch_items,
        "products": products,
        "orders": orders,
        "vehicles": vehicles,
        "drivers": drivers,
        "invoices": invoices,
        
        # Current filter values
        "current_product": product_name,
        "current_vehicle": vehicle_number,
        "current_driver": driver_name,
        "current_delivery_type": delivery_type,
        "current_status": status,
        "current_invoice": invoice_number,
        "type_selected": type_filter,
        "min_range_selected": min_range,
        "max_range_selected": max_range,
        
        # Totals
        "total_pre": total_pre,
        "total_std": total_std,
        "total_eco": total_eco,
        "total_com": total_com,
        "total_all": total_all,
        
        # Count of active dimensions (items)
        "active_dimensions": dispatch_items.count(),
    }

    return render(request, "logistics/index.html", context)




@login_required(login_url="login")
def add_dispatch(request):

    if request.method == "POST":

        dispatch_form = DispatchForm(request.POST)
        item_form = DispatchItemForm(request.POST)

        if dispatch_form.is_valid() and item_form.is_valid():

            order = dispatch_form.cleaned_data["order"]

            dispatch = dispatch_form.save()

            dispatch_item = item_form.save(commit=False)

            dispatch_item.dispatch_id = dispatch
            dispatch_item.product_id = order.product

            dispatch_item.pre_quantity = min(dispatch_item.pre_quantity, order.pre_quantity)
            dispatch_item.std_quantity = min(dispatch_item.std_quantity, order.std_quantity)
            dispatch_item.com_quantity = min(dispatch_item.com_quantity, order.com_quantity)
            dispatch_item.eco_quantity = min(dispatch_item.eco_quantity, order.eco_quantity)

            dispatch_item.total_quantity = (
                dispatch_item.pre_quantity +
                dispatch_item.std_quantity +
                dispatch_item.com_quantity +
                dispatch_item.eco_quantity
            )

            if dispatch_item.total_quantity >= order.total_quantity:
                dispatch.delivery_type = "full"
            else:
                dispatch.delivery_type = "partial"

            dispatch.save()

            dispatch_item.weight = dispatch.total_weight
            dispatch_item.save()

            messages.success(request, "Dispatch created successfully!")
            return redirect("logistics_view")

        else:
            print("Dispatch Errors:", dispatch_form.errors)
            print("Item Errors:", item_form.errors)

    else:
        dispatch_form = DispatchForm()
        item_form = DispatchItemForm()

    return render(request, "logistics/add_dispatch.html", {
        "dispatch_form": dispatch_form,
        "item_form": item_form,
        "orders": Order.objects.all().order_by('-ord_id'),
    })



@login_required(login_url="login")
def update_dispatch_status(request, dispatch_id):

    if request.method == "POST":
        try:
            dispatch = Dispatch.objects.get(id=dispatch_id)

            new_status = request.POST.get("status")

            if new_status in ["in-transit", "delivered"]:
                dispatch.status = new_status
                dispatch.save()

        except Dispatch.DoesNotExist:
            pass

    return redirect("logistics_view")



@login_required(login_url="login")
def print_invoice(request, dispatch_id):

    dispatch = Dispatch.objects.get(id=dispatch_id)
    items = DispatchItem.objects.filter(dispatch_id=dispatch)

    subtotal = 0

    for item in items:
        subtotal += item.total_quantity

    cgst = subtotal * 0.09
    sgst = subtotal * 0.09
    grand_total = subtotal + cgst + sgst

    context = {
        "dispatch": dispatch,
        "items": items,
        "subtotal": subtotal,
        "cgst": cgst,
        "sgst": sgst,
        "grand_total": grand_total,
    }

    return render(request, "logistics/print_invoice.html", context)