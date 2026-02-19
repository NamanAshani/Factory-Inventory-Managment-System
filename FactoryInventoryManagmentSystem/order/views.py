from django.shortcuts import render, get_object_or_404
from .models import Order

def order_home(request):
    return render(request, "order/index.html")

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

    return render(request, "order/order_details.html", {
        "order": order
    })
