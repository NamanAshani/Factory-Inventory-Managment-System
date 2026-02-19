from django.shortcuts import render, redirect
from .models import Customer
from django.shortcuts import get_object_or_404
from order.models import Order

def add_customer(request):

    if request.method == "POST":

        customer_name = request.POST.get("customer_name")
        phone_no = request.POST.get("phone_no")
        customer_city = request.POST.get("customer_city")
        remark = request.POST.get("remark")
        type = request.POST.get("type")
        truck_no = request.POST.get("truck_no")
        ref_party = request.POST.get("ref_party")

        Customer.objects.create(
            customer_name=customer_name,
            phone_no=phone_no,
            customer_city=customer_city,
            remark=remark,
            type=type,
            truck_no=truck_no,
            ref_party=ref_party
        )

        return redirect("customer_list")

    return render(request, "customer/add_customer.html")


def customer_list(request):

    customers = Customer.objects.all().order_by('-customer_date')

    return render(request, "customer/customer_list.html", {
        "customers": customers
    })


def customer_details(request, pk):

    customer = get_object_or_404(Customer, pk=pk)
    orders = Order.objects.filter(cust_name=customer)

    return render(request, "customer/customer_details.html", {
        "customer": customer,
        "orders": orders
    })
