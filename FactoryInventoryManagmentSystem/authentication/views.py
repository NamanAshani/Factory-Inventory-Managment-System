# import render and redirect for page navigation
from django.shortcuts import render, redirect

# import authenticate and login functions
from django.contrib.auth import authenticate, login

# import messages to show error text on login page
from django.contrib import messages

#for marketing
from customer.models import Customer
from order.models import Order
from django.shortcuts import get_object_or_404


# login view function
def login_view(request):

    # check if form submitted
    if request.method == "POST":

        # get username from form
        username = request.POST.get("username")

        # get password from form
        password = request.POST.get("password")

        selected_role = request.POST.get("role") 

        # check credentials using django auth system
        user = authenticate(request, username=username, password=password)

        # if user exists and password correct
        if user is not None:

            # Check if selected role matches actual group
            if not user.groups.filter(name=selected_role.replace("_", " ").title()).exists():
                messages.error(request, "❌ Selected role does not match your account")
                return redirect("login")

            # log user into session
            login(request, user)

            # redirect user based on role (group)

            if user.groups.filter(name="Management Director").exists():
                return redirect("md_dashboard")

            elif user.groups.filter(name="Management Head").exists():
                return redirect("/mh_dashboard")

            elif user.groups.filter(name="Marketing Head").exists():
                return redirect("/mar_h_dashboard")
            
            elif user.groups.filter(name="Purchase Head").exists():
                return redirect("ph_dashboard")
            
            elif user.groups.filter(name="Account Head").exists():
                return redirect("/ah_dashboard")
            
            elif user.groups.filter(name="Dispatch Head").exists():
                return redirect("/dh_dashboard")

            # fallback redirect
            else:
                return redirect("/")

        else:
            # show message if username or password wrong
            messages.error(request, "❌ Invalid Username or Password")

            # render login page again
            return redirect("login") 

    # show login page if GET request
    return render(request, "login.html")


def ah_dashboard(request):
    return render(request, "Admin/ah_dashboard.html")

def dh_dashboard(request):
    return render(request, "Admin/dh_dashboard.html")


def mar_h_dashboard(request):

    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()

    context = {
        "total_customers": total_customers,
        "total_orders": total_orders,
    }

    return render(request, "Admin/mar_h_dashboard.html", context)


def md_dashboard(request):
    return render(request, "Admin/md_dashboard.html")

def mh_dashboard(request):
    return render(request, "Admin/mh_dashboard.html")

def ph_dashboard(request):
    return render(request, "Admin/ph_dashboard.html")






#marketing views

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


def order_list(request):

    orders = Order.objects.select_related('cust_name','product').all().order_by('-ord_date')

    return render(request, "order/order_list.html", {
        "orders": orders
    })


def order_details(request, pk):

    order = get_object_or_404(Order, pk=pk)

    return render(request, "order/order_details.html", {
        "order": order
    })
