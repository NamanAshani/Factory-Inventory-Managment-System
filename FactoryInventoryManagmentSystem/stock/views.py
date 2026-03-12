from django.contrib import messages

from django.shortcuts import render,redirect
from .models import Stock,Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def index(request):

    stocks = Stock.objects.select_related('product').all()

    product = ""
    brand = ""
    design = ""
    type_filter = ""
    min_range = ""
    max_range = ""
   

    if request.method == "POST":
        

        product = request.POST.get('product')
        brand = request.POST.get('brand')
        design = request.POST.get('design')
        type_filter = request.POST.get('type')
        min_range = request.POST.get('min_range')   
        max_range = request.POST.get('max_range')  

        

       
        if product:
            stocks = stocks.filter(product__pro_name__icontains=product)

        if brand:
            stocks = stocks.filter(product__brand=brand)

        if design:
            stocks = stocks.filter(product__design=design)

       
        field_map = {
            "pre": "pre_quantity",
            "eco": "eco_quantity",
            "com": "com_quantity",
            "std": "std_quantity",
            "total": "total_quantity",
        }

        if type_filter in field_map:
            field = field_map[type_filter]
            filters = {}

            try:
                min_val = int(min_range) if min_range else None
                max_val = int(max_range) if max_range else None

                
                if min_val is not None and max_val is not None:
                    if min_val > max_val:
                        min_val, max_val = max_val, min_val

                if min_val is not None:
                    filters[f"{field}__gte"] = min_val

                if max_val is not None:
                    filters[f"{field}__lte"] = max_val

                if filters:
                    stocks = stocks.filter(**filters)

            except ValueError:
                pass 

    context = {
        "stocks": stocks,
        "product_selected": product,
        "brand_selected": brand,
        "design_selected": design,
        "type_selected": type_filter,
        "min_range_selected": min_range,
        "max_range_selected": max_range,
       
    }

    return render(request, "Stock/index.html", context)




@login_required(login_url="login")
def add_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid():
        product = form.save()
        if not Stock.objects.filter(product=product).exists():
            Stock.objects.create(product=product)       
        return redirect('index')  # change to your dashboard url name

    return render(request, 'Stock/add_product.html', {'form': form})



@login_required(login_url="login")
def add_stock(request):
    products = Product.objects.all()

    if request.method == "POST":
        pro_id = request.POST.get("product")
        action = request.POST.get("action")

        if not pro_id:
            messages.error(request, "Please select a product.")
            return redirect("add_stock")

        if action not in ["add", "remove", "update"]:
            messages.error(request, "Invalid action selected.")
            return redirect("add_stock")

        stock, created = Stock.objects.get_or_create(product_id=pro_id)

        pre_qty = int(request.POST.get("pre_quantity") or 0)
        std_qty = int(request.POST.get("std_quantity") or 0)
        com_qty = int(request.POST.get("com_quantity") or 0)
        eco_qty = int(request.POST.get("eco_quantity") or 0)

        if action == "add":
            stock.pre_quantity += pre_qty
            stock.std_quantity += std_qty
            stock.com_quantity += com_qty
            stock.eco_quantity += eco_qty
            messages.success(request, "Stock added successfully.")

        elif action == "remove":
            stock.pre_quantity = max(0, stock.pre_quantity - pre_qty)
            stock.std_quantity = max(0, stock.std_quantity - std_qty)
            stock.com_quantity = max(0, stock.com_quantity - com_qty)
            stock.eco_quantity = max(0, stock.eco_quantity - eco_qty)
            messages.success(request, "Stock removed successfully.")

        elif action == "update":
            stock.pre_quantity = pre_qty
            stock.std_quantity = std_qty
            stock.com_quantity = com_qty
            stock.eco_quantity = eco_qty
            messages.success(request, "Stock updated successfully.")

        stock.save()
        return redirect("add_stock")

    return render(request, "Stock/add_stock.html", {"products": products})
     

    return render(request, 'Stock/add_stock.html', {'products': products})