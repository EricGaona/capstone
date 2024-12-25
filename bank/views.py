from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from .models import User
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    # user = User.objects.get(username=request.user.username)  DA ERROR SI NO ESTA LOGUEADO
    # users = User.objects.all()
    # print(f"SOY user ---QuerySet--- >>> {users}")
    # print(" ----- 1 -------------- ")
    # users_json = User.objects.all().values()
    # print(f"SOY user_json ----- >>> {users_json}")
    # print(" ----- 2 -------------- ")

    test = "world!"
    return render(request, "bank/index.html", {
        "test": test
    })

@csrf_exempt
def register(request):
    if request.method == "POST":
        print(request.POST) 
        username = request.POST["username"]
        email = request.POST["email"]
        print(f"SOY EMAIL --- >>> {email}")
        print(f"SOY USERNAME --- >>> {username}")
        
    else:
        return render(request, "auctions/register.html")