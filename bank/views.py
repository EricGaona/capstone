import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
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
import requests
from dotenv import load_dotenv, dotenv_values


VONAGE_API_KEY = os.getenv('VONAGE_API_KEY') 
VONAGE_API_SECRET = os.getenv('VONAGE_API_SECRET')

# Create your views here.

def index(request):
    print("------- 1 -------")
    print(VONAGE_API_KEY)
    print(VONAGE_API_SECRET)
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
        email = email.lower()
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
            email = email.lower()
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


@csrf_exempt
def send_money(request):
    recipient_email = ""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            sender_account_number = data.get("senderAccountNumber")
            recipient_email = data.get("recipientEmail").lower()

            user_recipient = User.objects.get(email=recipient_email)
            recipient_account_number = user_recipient.account_number

            user_sender = User.objects.get(account_number = sender_account_number)

            phone_number = user_sender.phone_number
            print(f"SOY PHONE_NUMBER --- >>> {phone_number}")
            amount = float(data.get("amount"))

            if amount <= 0:
                return JsonResponse({"error": "Amount must be greater than zero."}, status=400)

            if not all([sender_account_number, recipient_account_number, amount]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            try:
                sender = User.objects.get(account_number=sender_account_number)
                recipient = User.objects.get(account_number=recipient_account_number)
                
                if sender == recipient:
                    return JsonResponse({"error": f"The email <b>{recipient_email}</b> is your own email."}, status=400)
            except User.DoesNotExist:
                return JsonResponse({"error": "One or both account numbers are invalid."}, status=400)

            if sender.balance < amount:
                return JsonResponse({"error": "Insufficient funds."}, status=400)

            # Trigger Vonage code validation
          
            url = f"https://api.nexmo.com/verify/json?api_key={VONAGE_API_KEY}&api_secret={VONAGE_API_SECRET}&number={phone_number}&brand=AcmeInc"
         
            response = requests.get(url)
            verification_data = response.json()

            if verification_data['status'] == '0':
                request_id = verification_data['request_id']
                request.session['verification_request_id'] = request_id
                request.session['transfer_data'] = data  # Save transfer data in session
                return JsonResponse({"message": "Check your phone for a verification code."}, status=200)
            else:
                return JsonResponse({"error": "Failed to initiate verification."}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        except Exception as e:
            print("Entro Aqui ---- >> ")
            message = f"The email <b>{recipient_email}</b> does not exist on the database."
            return JsonResponse({"error": str(message)}, status=500)
            
            # return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)



@csrf_exempt
def validate_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(f"SOY DATA -- >>>{data}")
            code = data.get("code")
            print(f"SOY CODE -- >>>{code}")
                                                                                 # request_id = data.get("request_id")
            request_id = request.session.get('verification_request_id')
            print(f"SOY REQUEST_ID -- >>>{request_id}")
            if not request_id:
                return JsonResponse({"error": "No verification request found."}, status=400)

            url = f"https://api.nexmo.com/verify/check/json?api_key={VONAGE_API_KEY}&api_secret={VONAGE_API_SECRET}&request_id={request_id}&code={code}"
            response = requests.get(url)
            validation_data = response.json()
            status = validation_data['status']
            print(f"SOY status  --- >>> {status}")


            if validation_data['status'] == '0':
                # Code validated successfully, proceed with money transfer
                transfer_data = request.session.get('transfer_data')
                if transfer_data:
                    sender = User.objects.get(account_number=transfer_data['senderAccountNumber'])
                    recipient_email = transfer_data['recipientEmail'].lower()
                    recipient = User.objects.get(email=recipient_email)
                    amount = float(transfer_data['amount'])

                    if sender.balance >= amount:
                        sender.balance -= amount
                        recipient.balance += amount
                        sender.save()
                        recipient.save()
                        return JsonResponse({"success": True, "message": "Money sent successfully!"}, status=200)
                    else:
                        return JsonResponse({"success": False, "error": "Insufficient funds."}, status=400)
                else:
                    return JsonResponse({"success": False, "error": "Transfer data not found."}, status=400)
            else:
                 # Cancel the verification request
                cancel_url = f"https://api.nexmo.com/verify/control/json?api_key={VONAGE_API_KEY}&api_secret={VONAGE_API_SECRET}&request_id={request_id}&cmd=cancel"
                # requests.get(cancel_url)
                print("Entro A Cancel --- >>>")

                cancel_response = requests.get(cancel_url)

                # You can also check the cancel_response for success/failure if necessary
                print(f"Cancel response: {cancel_response.json()}")
                return JsonResponse({"success": False, "error": "Invalid verification code. The process has been cancelled."}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        except Exception as e:
            print("Entro aqui tambien ---2 >>>")
            print(f"Error in validate_code: {e}")
            return JsonResponse({"error": str(e
            )}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


def loan(request, username):
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

    return render(request, "bank/loan.html", {
        "user_name": user_name,
    })
