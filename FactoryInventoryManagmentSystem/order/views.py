from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'login.html')
# def login_view(request, role):
#     print(role)  
#     return render(request, f"{role}/login.html", {"role": role})
