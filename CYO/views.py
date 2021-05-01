from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Adventure, Event, Choice

class new_Adventure(forms.ModelForm):
    class Meta:
        model = Adventure
        exclude = ["user", "startevent"]
        fields = ["title", "description"]

class new_Event(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ["adventure"]
        fields = ["title", "text"]

def index_view(request):
    return render(request, "CYO/index.html")

def create_view(request):
    if request.method == "GET":
        form = new_Adventure()
        return render(request, "CYO/create.html", {
            "form": form
        })
    elif request.method == "POST":
        adventure = new_Adventure(request.post)
        if adventure.is_valid:
            adventure.save(commit=False)
            adventure.user = request.user
            adventure.save()
            first_event = new_Event()
            first_event.title = adventure.title
            first_event.adventure = adventure
            first_event.text = adventure.description
        pass

def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "CYO/error.html",
            {
                "message": "No such user"
            })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))        

def register_view(request):
    if request.method == "GET":
        return render(request, "CYO/register.html")
    if request.method == "POST":
        username = request.POST["username"]
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
        login(request, user)
        return HttpResponseRedirect(reverse('index'))