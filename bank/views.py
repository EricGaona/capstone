from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.db import IntegrityError
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import random
# Create your views here.

def index(request):
    # user = User.objects.get(username=request.user.username)  DA ERROR SI NO ESTA LOGUEADO
    # users = User.objects.all()
    # print(f"SOY user ---QuerySet--- >>> {users}")
    # print(" ----- 1 -------------- ")
    # users_json = User.objects.all().values()
    # print(f"SOY user_json ----- >>> {users_json}")
    # print(" ----- 2 -------------- ")

    user = request.user
    return render(request, "bank/index.html", {
        "test": user
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["userName"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "bank/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "bank/login.html")
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def generate_unique_account_number():
    """Generate a unique account number."""
    while True:
        account_number = random.randint(1000000000, 9999999999)  # 10-digit number
        if not User.objects.filter(account_number=account_number).exists():
            return account_number


def register(request):
    if request.method == "POST":
        # Retrieve data from the POST request
        username = request.POST["userName"] 
        first_name = request.POST["firstName"]
        last_name = request.POST["lastName"]
        email = request.POST["email"]
        phone_number = request.POST["phoneNumber"]  
        address = request.POST["address"]   
        password = request.POST["password"]
        confirm_password = request.POST["confirmPassword"]  
        

        # Validate required fields
        if not all([username, first_name, last_name, email, phone_number, address, password, confirm_password]):
            # return JsonResponse({"error": "All fields are required."}, status=400)
            return render(request, "bank/register.html", {
                "message": "All fields are required."
                })

        # Validate passwords match
        if password != confirm_password:
            # return JsonResponse({"error": "Passwords do not match."}, status=400)
            return render(request, "bank/register.html", {
                "message": "Passwords do not match."
                })

        # Generate unique account number
        account_number = generate_unique_account_number()

        # Create a new user (ensure your model matches these fields)
        try:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                address=address,
                account_number=account_number,
                password=password  
            )
            user.save()
            # return JsonResponse({"message": "User registered successfully!", "accountNumber": account_number}, status=201)
        except IntegrityError:
            return render(request, "bank/register.html", {
                "message": "Username already taken."
                })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "bank/register.html")  # Render the registration form

    

