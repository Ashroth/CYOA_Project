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
        exclude = ["user", "startevent", "endevent"]
        fields = ["title", "description"]

class new_Event(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ["adventure"]
        fields = ["title", "text"]

class new_Choice(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ['initial', 'final']
        fields = ['text', 'condition_amount']

def index_view(request):
    return render(request, "CYO/index.html")

def create_view(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        form = new_Adventure()
        return render(request, "CYO/create.html", {
            "form": form
        })
    elif request.method == "POST":
        adventure = new_Adventure(request.post)
        if adventure.is_valid:
            adventure.save(commit=False)
            adventure.user = request.user
            first_event = Event(text = adventure.cleaned_data["description"], adventure = adventure, title = adventure.cleaned_data["title"])
            first_event.save()
            last_event = Event(text = "This is the default end screen", adventure = adventure, title = "Ending")
            last_event.save()
            adventure.startevent = first_event
            adventure.endevent = last_event
            adventure.save()
            choice = Choice(initial = last_event, final = first_event, condition_amount = 0, text = "Back to the start screen")
            choice.save()
            return HttpResponseRedirect(reverse('edit', kwargs = {'ad_index': adventure.cleaned_data['id']}))
        pass

def event_create_view(request, ad_index):
    if request.method == "GET":
        form = new_Event()
        return render(request, 'create.html', {
            "form": form
        })
    if request.method == "POST":
        event = new_Event(request.post)
        if event.is_valid:
            event.save(commit = False)
            event.adventure = Adventure.objects.get(id = ad_index)
            event.save()
            return HttpResponseRedirect(reverse('edit', kwargs = {'ad_index': ad_index}))
        else:
            return render(request, 'error.html', {
                "message": "Faulty form"
            })

def choice_create_view(request, ev_index):
    if request.method == "GET":
        form = new_Choice()
        return render (request, 'create.html', {
            "form": form
        })

def adventure_edit_view(request, ad_index):
    if request.method == "GET":
        try:
            adventure = Adventure.objects.get(id = ad_index)
        except Adventure.DoesNotExist:
            return render(request, 'error.html', {
                "message": "No such adventure"
            })
        return render(request, 'adventureedit.html', {
            "adventure": adventure
        })

def event_edit_view(request, ad_index, ev_index):
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