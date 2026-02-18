from django.shortcuts import render

def order_home(request):
    return render(request, "order/index.html")
