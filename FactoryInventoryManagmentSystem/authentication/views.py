# import render and redirect for page navigation
from django.shortcuts import render, redirect

# import authenticate and login functions
from django.contrib.auth import authenticate, login

# import messages to show error text on login page
from django.contrib import messages


# login view function
def login_view(request):

    # check if form submitted
    if request.method == "POST":

        # get username from form
        username = request.POST.get("username")

        # get password from form
        password = request.POST.get("password")

        # check credentials using django auth system
        user = authenticate(request, username=username, password=password)

        # if user exists and password correct
        if user is not None:

            # log user into session
            login(request, user)

            # redirect user based on role (group)

            if user.groups.filter(name="Management Director").exists():
                return redirect("/director_dashboard")

            elif user.groups.filter(name="Management Head").exists():
                return redirect("/management_dashboard")

            elif user.groups.filter(name="Marketing Head").exists():
                return redirect("/marketing_dashboard")
            
            elif user.groups.filter(name="Purchase Head").exists():
                return redirect("/purchase_dashboard")
            
            elif user.groups.filter(name="Account Head").exists():
                return redirect("/account_dashboard")
            
            elif user.groups.filter(name="Dispatch Head").exists():
                return redirect("/dispatch_dashboard")

            # fallback redirect
            else:
                return redirect("/")

        else:
            # show message if username or password wrong
            messages.error(request, "❌ Invalid Username or Password")

            # render login page again
            return render(request, "login.html")

    # show login page if GET request
    return render(request, "login.html")
