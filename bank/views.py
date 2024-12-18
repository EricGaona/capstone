from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .models import User
# Create your views here.

def index(request):
    test = "world!"
    return render(request, "bank/index.html", {
        "test": test
    })