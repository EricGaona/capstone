from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .models import User
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