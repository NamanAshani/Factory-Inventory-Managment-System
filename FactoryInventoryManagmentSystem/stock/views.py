from django.shortcuts import render
from .models import Stock,Product


def index(request):

    stocks = Stock.objects.select_related('product').all()

    product = ""
    brand = ""
    design = ""
    type_filter = ""
    min_range = ""
    max_range = ""
    total_products = Product.objects.count()

    if request.method == "POST":
        

        product = request.POST.get('product')
        brand = request.POST.get('brand')
        design = request.POST.get('design')
        type_filter = request.POST.get('type')
        min_range = request.POST.get('min_range')   # ✅ MATCH HTML
        max_range = request.POST.get('max_range')   # ✅ MATCH HTML

        print("TYPE:", type_filter)
        print("MIN:", min_range)
        print("MAX:", max_range)

        # Basic filters
        if product:
            stocks = stocks.filter(product__pro_name__icontains=product)

        if brand:
            stocks = stocks.filter(product__brand=brand)

        if design:
            stocks = stocks.filter(product__design=design)

        # Quantity field mapping
        field_map = {
            "pre": "pre_quantity",
            "eco": "eco_quantity",
            "com": "com_quantity",
            "std": "std_quantity",
        }

        if type_filter in field_map:
            field = field_map[type_filter]
            filters = {}

            try:
                min_val = int(min_range) if min_range else None
                max_val = int(max_range) if max_range else None

                # 🔥 Protection: swap if user enters wrong order
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
                pass  # ignore invalid numbers safely

    context = {
        "stocks": stocks,
        "product_selected": product,
        "brand_selected": brand,
        "design_selected": design,
        "type_selected": type_filter,
        "min_range_selected": min_range,
        "max_range_selected": max_range,
        "total_products": total_products,
    }

    return render(request, "Stock/index.html", context)