from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Order
from stock.models import Product
from customer.models import Customer
from django.db.models import Q
from django.contrib import messages


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

