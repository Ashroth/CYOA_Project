from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError, models
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
        exclude = ['initial']
        fields = ['text', 'condition_amount', 'final']

def index_view(request):
    if request.method == "GET":
        adventures = Adventure.objects.all()
    return render(request, "CYO/index.html", {
        "adventures": adventures
    })

def create_view(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        form = new_Adventure()
        return render(request, "CYO/create.html", {
            "form": form,
            "type": "Create an adventure"
        })
    elif request.method == "POST":
        adventure = new_Adventure(request.POST)
        if adventure.is_valid:
            adventure = adventure.save(commit=False)
            adventure.user = request.user
            first_event = Event(text = adventure.description, adventure = adventure, title = adventure.title)
            last_event = Event(text = "This is the default end screen", adventure = adventure, title = "Ending")
            adventure.save()
            first_event.save()
            last_event.save()
            adventure.startevent = first_event
            adventure.endevent = last_event
            adventure.save()
            choice = Choice(initial = last_event, final = first_event, condition_amount = 0, text = "Back to the start screen")
            choice.save()
            return HttpResponseRedirect(reverse('ad_edit', kwargs = {'ad_index': adventure.id}))

def event_create_view(request, ad_index):
    if request.method == "GET":
        form = new_Event()
        return render(request, 'CYO/create.html', {
            "form": form,
            "type": "Create an event"
        })
    if request.method == "POST":
        event = new_Event(request.POST)
        if event.is_valid:
            event = event.save(commit = False)
            event.adventure = Adventure.objects.get(id = ad_index)
            event.save()
            return HttpResponseRedirect(reverse('ev_edit', kwargs = {'event_index': event.id}))
        else:
            return render(request, 'CYO/error.html', {
                "message": "Faulty form"
            })

def choice_create_view(request, event_index):
    if request.method == "GET":
        adventure = Event.objects.get(id = event_index).adventure
        form = new_Choice()
        form.fields['final'] = forms.ModelChoiceField(queryset = Event.objects.filter(adventure = adventure))
        return render (request, 'CYO/create.html', {
            "form": form,
            "type": "Create a choice"
        })
    if request.method == "POST":
        choice = new_Choice(request.POST)
        adventure = Event.objects.get(id = event_index).adventure
        choice.fields['final'] = forms.ModelChoiceField(queryset = Event.objects.filter(adventure = adventure))
        if choice.is_valid:
            choice = choice.save(commit = False)
            choice.initial = Event.objects.get(id = event_index)
            choice.save()
            return HttpResponseRedirect(reverse('ev_edit', kwargs = {'event_index': event_index}))
        return render(request, 'CYO/error.html', {
            "message": "Faulty form"
        })
        

def adventure_edit_view(request, ad_index):
    if request.method == "GET":
        try:
            adventure = Adventure.objects.get(id = ad_index)
        except Adventure.DoesNotExist:
            return render(request, 'error.html', {
                "message": "No such adventure"
            })
        return render(request, 'CYO/adventureedit.html', {
            "adventure": adventure
        })

def event_edit_view(request, event_index):
    if request.method == "GET":
        try:
            event = Event.objects.get(id = event_index)
        except Event.DoesNotExist:
            return render(request, 'error.html', {
                "message": "No such event"
            })
        return render(request, 'CYO/edit.html', {
            "event": event
        })

def adventure_view(request, adventure_index):
    if request.method == "GET":
        try:
            adventure = Adventure.objects.get(id = adventure_index)
        except Adventure.DoesNotExist:
            return render(request, 'CYO/error.html',
            {
                "message": "No such adventure"
            })
        return render(request, 'CYO/adventure_view.html', 
        {
            "adventure": adventure
        })

def adventure_event_view(request, event_index):
    if request.method == "GET":
        try:
            event = Event.objects.get(id = event_index)
        except Event.DoesNotExist:
            return JsonResponse(status = 404
            )
        choices_temp = event.Start.all()
        choices = []
        for choice in choices_temp:
            choices.append([choice.final.id, choice.text, choice.condition_amount])
        return JsonResponse({
            "title": event.title,
            "text": event.text,
            "choices": choices
        }, status = 200)

def login_view(request):
    if request.method == "GET":
        return render(request, "CYO/login.html")
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