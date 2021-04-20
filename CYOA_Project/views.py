from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django import forms

def login_view(request):
    pass

def register_view(request):
    if request.method == "GET":
        return render(request, "register.html")
    if request.method == "POST":
        user = request.POST["user"]
        password = request.POST["password"]
        confirm = request.POST["confirm"]
        email = request.POST["email"]
        if password != confirm:
            pass
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            pass
        login(request.user)
        return HttpResponseRedirect(reverse('index'))