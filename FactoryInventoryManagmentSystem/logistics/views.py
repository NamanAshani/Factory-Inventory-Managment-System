from pyexpat.errors import messages
from django.shortcuts import render, redirect
from .models import Dispatch, DispatchItem
from stock.models import Product
from order.models import Order
from django.contrib.auth.decorators import login_required
from .forms import DispatchForm, DispatchItemForm, DispatchCreateForm

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
    orders = Order.objects.all().order_by('-ord_id')
    context = {
        "orders": orders
    }
    return render(request, "logistics/add_dispatch.html", context)


@login_required(login_url="login")
def create_dispatch(request):
    if request.method == "POST":
        # Get form data
        order_id = request.POST.get('order_id')
        vehicle_number = request.POST.get('vehicle_number')
        driver_name = request.POST.get('driver_name')
        total_weight = request.POST.get('total_weight')
        delivery_type = request.POST.get('delivery_type')
        status = request.POST.get('status')
        invoice_number = request.POST.get('invoice_number')
        
        try:
            # Get the order
            order = Order.objects.get(ord_id=order_id)
            
            # Create dispatch
            dispatch = Dispatch.objects.create(
                order=order,
                vehicle_number=vehicle_number,
                driver_name=driver_name,
                total_weight=total_weight,
                delivery_type=delivery_type,
                status=status,
                invoice_number=invoice_number
            )
            
            # messages.success(request, 'Dispatch created successfully!')
            return redirect('logistics_view')
            
        except Order.DoesNotExist:
            messages.error(request, 'Selected order does not exist.')
            return redirect('add_dispatch')
        except Exception as e:
            messages.error(request, f'Error creating dispatch: {str(e)}')
            return redirect('add_dispatch')
    
    return redirect('logistics_view')
# @login_required(login_url="login")
# def create_dispatch(request):
#     if request.method == "POST":
#         # Get form data
#         order_id = request.POST.get('order_id')
#         vehicle_number = request.POST.get('vehicle_number')
#         driver_name = request.POST.get('driver_name')
#         total_weight = request.POST.get('total_weight')
#         delivery_type = request.POST.get('delivery_type')
#         status = request.POST.get('status')
#         invoice_number = request.POST.get('invoice_number')
        
#         # Create dispatch
#         order = Order.objects.get(ord_id=order_id)
#         dispatch = Dispatch.objects.create(
#             order=order,
#             vehicle_number=vehicle_number,
#             driver_name=driver_name,
#             total_weight=total_weight,
#             delivery_type=delivery_type,
#             status=status,
#             invoice_number=invoice_number
#         )
        
#         # Here you would typically create DispatchItems based on the order
#         # This is just a placeholder - you'll need to implement based on your business logic
        
#         return redirect('logistics_view')
    
#     return redirect('logistics_view')