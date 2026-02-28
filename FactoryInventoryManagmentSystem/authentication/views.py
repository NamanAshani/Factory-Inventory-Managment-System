# import render and redirect for page navigation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# import authenticate and login functions
from django.contrib.auth import authenticate, login

# import messages to show error text on login page
from django.contrib import messages

#for marketing
from customer.models import Customer
from order.models import Order
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout

# for management director dashboard
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from stock.models import Stock
from account.models import Invoice





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


@login_required(login_url="login")
def ah_dashboard(request):
    return render(request, "Admin/ah_dashboard.html")

@login_required(login_url="login")
def dh_dashboard(request):
    return render(request, "Admin/dh_dashboard.html")

@login_required(login_url="login")
def mar_h_dashboard(request):

    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()

    context = {
        "total_customers": total_customers,
        "total_orders": total_orders,
    }

    return render(request, "Admin/mar_h_dashboard.html", context)



@login_required(login_url="login")
def md_dashboard(request):

    # role protection (VERY IMPORTANT)
    if not request.user.groups.filter(name="Management Director").exists():
        return redirect("login")

    # total orders
    total_orders = Order.objects.count()

    # total revenue
    total_revenue = Invoice.objects.aggregate(
        Sum("total_amount")
    )["total_amount__sum"] or 0

    # total pending (using balance property)
    total_pending = sum(
        invoice.balance_amount for invoice in Invoice.objects.all()
    )

    # total stock
    total_stock = Stock.objects.aggregate(
        Sum("total_quantity")
    )["total_quantity__sum"] or 0

    # recent orders
    recent_orders = Order.objects.order_by("-ord_date")[:5]

    # top customers
    top_customers = Customer.objects.order_by("-cus_quantity")[:5]

    context = {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "total_pending": total_pending,
        "total_stock": total_stock,
        "recent_orders": recent_orders,
        "top_customers": top_customers,
    }
    return render(request, "Admin/md_dashboard.html", context)



@login_required(login_url="login")
def mh_dashboard(request):

    # ---------------------------
    # SUMMARY DATA
    # ---------------------------

    total_orders = Order.objects.count()

    pending_orders = Order.objects.filter(status="pending").count()

    delivered_orders = Order.objects.filter(status="delivered").count()

    total_stock = Stock.objects.aggregate(
        Sum("total_quantity")
    )["total_quantity__sum"] or 0

    # ---------------------------
    # RECENT ORDERS
    # ---------------------------

    recent_orders = Order.objects.select_related(
        "cust_name",
        "product"
    ).order_by("-ord_date")[:5]

    context = {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
        "total_stock": total_stock,
        "recent_orders": recent_orders,
    }

    return render(request, "Admin/mh_dashboard.html", context)

@login_required(login_url="login")
def ph_dashboard(request):
    return render(request, "Admin/ph_dashboard.html")
