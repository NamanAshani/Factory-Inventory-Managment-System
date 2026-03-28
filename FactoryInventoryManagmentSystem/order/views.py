from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Order
from stock.models import Product
from customer.models import Customer
from django.db.models import Q, Sum
from django.contrib import messages
from stock.models import Stock

def order_home(request):
    orders = Order.objects.select_related('cust_name', 'product').all().order_by('-ord_date')

    # GET filters
    status = request.GET.get("status", "").strip()
    order_type = request.GET.get("order_type", "").strip()
    q = request.GET.get("q", "").strip()

    if status:
        orders = orders.filter(status=status)

    if order_type:
        orders = orders.filter(order_type=order_type)

    if q:
        orders = orders.filter(
            Q(cust_name__customer_name__icontains=q) |   # change cus_name if your Customer field name is different
            Q(product__pro_name__icontains=q) |     # change pro_name if Product field name is different
            Q(product__brand__icontains=q) |
            Q(product__design__icontains=q)
        )

    # dropdown values
    order_types = (
        Order.objects.exclude(order_type__isnull=True)
        .exclude(order_type__exact="")
        .values_list("order_type", flat=True)
        .distinct()
        .order_by("order_type")
    )

    # counts should be from ALL orders (not filtered), so use base queryset:
    all_orders = Order.objects.all()
    return render(request, "order/index.html", {
        "orders": orders,
        "order_types": order_types,

        "total_orders": all_orders.count(),
        "pending_orders": all_orders.filter(status="pending").count(),
        "shipped_orders": all_orders.filter(status="shipped").count(),
        "delivered_orders": all_orders.filter(status="delivered").count(),
    })

def order_create(request):
    customers = Customer.objects.all().order_by("customer_name")
    products = Product.objects.all().order_by("pro_name")  

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("order_home")
        else:
            print("Please correct the errors below.",form.errors)
    else:
        form = OrderForm()

    return render(request, "order/order_create.html", {
        "form": form,
        "customers": customers,
        "products": products,
    })

def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("order_home")
    else:
        form = OrderForm(instance=order)

    customers = Customer.objects.all().order_by("customer_name")
    products = Product.objects.all()

    return render(request, "order/order_update.html", {
        "form": form,
        "order": order,
        "customers": customers,
        "products": products,
    })

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == "POST":
        order.delete()
        messages.success(request, "Order deleted successfully.")
        return redirect("order_home")

    return render(request, "order/order_confirm_delete.html", {"order": order})

def order_list(request):


    orders = Order.objects.select_related(
        'cust_name',
        'product'
    ).all().order_by('-ord_date')


    return render(request, "order/order_list.html", {
        "orders": orders
    })


def order_details(request, pk):
    order = get_object_or_404(Order, pk=pk)

    # get stock for the product
    stock = Stock.objects.filter(product=order.product).order_by('-total_quantity').first()
    stock_qty = stock.total_quantity if stock else 0

    # calculate remaining
    remaining = stock_qty - order.total_quantity

    return render(request, "order/order_details.html", {
        "order": order,
        "stock_qty": stock_qty,
        "remaining": remaining
    })

def order_magic(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    orders = (
        Order.objects
        .filter(product=product)
        .select_related('cust_name', 'product')
        .order_by('ord_date')
    )

    stock_qty = (
        Stock.objects
        .filter(product=product)
        .aggregate(total=Sum('total_quantity'))['total'] or 0
    )

    manual_mode = orders.filter(allocation_locked=True).exists()

    order_data = []
    current_stock = stock_qty

    for order in orders:
        if manual_mode:
            allocated = order.allocated_quantity
        else:
            allocated = min(current_stock, order.total_quantity)
            current_stock -= allocated

        remaining = allocated - order.total_quantity

        order_data.append({
            "order": order,
            "allocated_qty": allocated,
            "done_qty": allocated,
            "remaining": remaining,
        })

    total_allocated = sum(item["allocated_qty"] for item in order_data)
    remaining_stock = stock_qty - total_allocated

    return render(request, "order/order_magic.html", {
        "product": product,
        "stock_qty": stock_qty,
        "order_data": order_data,
        "total_allocated": total_allocated,
        "remaining_stock": remaining_stock,
        "manual_mode": manual_mode,
    })

from django.views.decorators.http import require_POST
from django.contrib import messages

@require_POST
def update_allocation(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    orders = Order.objects.filter(product=product).order_by('ord_date')

    stock_qty = (
        Stock.objects
        .filter(product=product)
        .aggregate(total=Sum('total_quantity'))['total'] or 0
    )

    total_allocated = 0
    cleaned_values = {}

    for order in orders:
        field_name = f"allocated_{order.ord_id}"
        raw_value = request.POST.get(field_name, "0").strip()

        try:
            qty = int(raw_value)
        except ValueError:
            qty = 0

        if qty < 0:
            qty = 0

        cleaned_values[order.ord_id] = qty
        total_allocated += qty

    if total_allocated > stock_qty:
        messages.error(
            request,
            f"Total allocation ({total_allocated}) exceeds available stock ({stock_qty})."
        )
        return redirect("order_magic", product_id=product.pro_id)

    for order in orders:
        order.allocated_quantity = cleaned_values[order.ord_id]
        order.allocation_locked = True
        order.save()

    messages.success(request, "Manual allocation saved successfully.")
    return redirect("order_magic", product_id=product.pro_id)

@require_POST
def reset_auto_allocation(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    orders = Order.objects.filter(product=product)

    for order in orders:
        order.allocated_quantity = 0
        order.allocation_locked = False
        order.save()

    messages.success(request, "Allocation reset to automatic mode.")
    return redirect("order_magic", product_id=product.pro_id)