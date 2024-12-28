from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.db import IntegrityError
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import random
from django.core.paginator import Paginator
# import logging
# logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    # user = User.objects.get(username=request.user.username)  DA ERROR SI NO ESTA LOGUEADO
    # users = User.objects.all()
    # print(f"SOY user ---QuerySet--- >>> {users}")
    # print(" ----- 1 -------------- ")
    # users_json = User.objects.all().values()
    # print(f"SOY user_json ----- >>> {users_json}")
    # print(" ----- 2 -------------- ")
    if request.user.is_authenticated:
        user = request.user
        account_number = user.account_number
        user_name = user.first_name
        return render(request, "bank/index.html", {
            "user_name": user_name,
            "account_number": account_number
        })
    else:
        return render(request, "bank/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "bank/login.html", {
                "message": "Invalid email and/or password."
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
        try:
            data = json.loads(request.body)

            # username = data.get("userName")
            first_name = data.get("firstName")
            last_name = data.get("lastName")
            email = data.get("email")
            phone_number = data.get("phoneNumber")
            address = data.get("address")
            password = data.get("password")
            confirm_password = data.get("confirmPassword")

            if not all([first_name, last_name, email, phone_number, address, password, confirm_password]):
                return JsonResponse({"error": "All fields are required."}, status=400)

            if password != confirm_password:
                return JsonResponse({"error": "Passwords do not match."}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already taken."}, status=400)
            if User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({"error": "Phone number already taken."}, status=400)

            account_number = generate_unique_account_number()

            user = User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                address=address,
                account_number=account_number,
                password=password
            )
            user.save()

            # Log in the user
            login(request, user)

            # Redirect to index.html on successful registration
            return JsonResponse({"message": "User registered successfully!", "accountNumber": account_number, "redirect": True}, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return render(request, "bank/register.html")

# @login_required
def profile(request, username):
    # user = User.objects.get(username=username)
    user = request.user
    user_name = user.first_name
    # posts = user.posts.all().order_by("-timestamp")
    # is_following = request.user.is_authenticated and user.followers.filter(follower=request.user).exists()
    # total_followers = user.followers.count()
    # total_following = user.following.count()

    # paginator = Paginator(posts, 10)
    # page_number = request.GET.get("page")
    # list_posts = paginator.get_page(page_number)

    return render(request, "bank/profile_page.html", {
        "user_name": user_name,
    })


# def custom_404_view(request, exception):
#     logger.debug("Custom 404 view triggered")
#     return render(request, "bank/404.html", status=404)
@csrf_exempt
def send_money(request):
    # Datos del usuario logueado
    user = request.user
    user_name = user.first_name
    print(f"SOY user_name >>> {user_name}")

    if request.method == "POST":
        data = json.loads(request.body)
        # Datos del usuario que viene por POST
        print(f"SOY DATA >>> {data}")
        id_user = data.get("id_user")
        print(f"SOY ID_USER >>> {id_user}")
        amount = data.get("amount")
        print(f"SOY AMOUNT >>> {amount}")
        print(" ----- 1 -------------- ")

        user = User.objects.get(id=id_user)
        print(f"SOY USER cash >>> {user.cash}")
        print(f"Soy UserName >>> {user.first_name}")
        print(f"Soy >>> {user}")

        return JsonResponse({"message": "Send money view."}, status=200)
    else:
    
        return JsonResponse({"message": "Error method."}, status=500)

