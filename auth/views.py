from django.shortcuts import render
from django.http import HttpResponse

def login_view(request): 
    return HttpResponse("Login Page")

# Create your views here.
