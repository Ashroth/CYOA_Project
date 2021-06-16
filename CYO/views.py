from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError, models
from django.http.response import HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django import forms
import json
from .models import User, Adventure, Event, Choice, Item, ItemStyle

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
        fields = ['text', 'final']

class new_Item(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ["event", "choice"]
        fields = ["itemstyle", "amount", "hidden"]

class new_ItemStyle(forms.ModelForm):
    class Meta:
        model = ItemStyle
        exclude = ["adventure"]
        fields = ["name", "type"]

def index_view(request):
    if request.method == "GET":
        adventures = Adventure.objects.all()
    return render(request, "CYO/index.html", {
        "adventures": adventures
    })

# Adventure creation code
@login_required
def adventure_create_view(request):
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
            item = ItemStyle(name = "Health", type = "Status", adventure = adventure)
            item.save()
            return HttpResponseRedirect(reverse('ad_edit', kwargs = {'index': adventure.id}))

@login_required
def adventure_edit_view(request, index):
    if request.method == "GET":
        try:
            adventure = Adventure.objects.get(id = index)
        except Adventure.DoesNotExist:
            return render(request, 'CYO/layout.html', {
                "message": "No such adventure"
            })
        if request.user == adventure.user:
            return render(request, 'CYO/adventureedit.html', {
                "adventure": adventure
            })
        else:
            return render(request, 'CYO/layout.html', {
                "message": "Only the creator may edit adventure"
            })

@login_required
def item_add_view(request, ad_index):
    if request.method == "GET":
        form = new_ItemStyle()
        return render(request, 'CYO/create.html', {
            "form": form,
            "type": "Create an item type for this adventure"
        })
    if request.method == "POST":
        item = new_ItemStyle(request.POST)
        adventure = Adventure.objects.get(id = ad_index)
        if item.is_valid and adventure.user == request.user:
            item = item.save(commit = False)
            item.adventure = adventure
            item.save()
            return HttpResponseRedirect(reverse('ad_edit', kwargs = {'index': ad_index}))
        elif not item.is_valid:
            return render(request, 'CYO/create.html', {
                "form": item,
                "message": "Invalid form"
            })
        else:
            return render(request, 'CYO/layout.html', {
                "message": "Only the creator may add items"
            })

# Event creation code
@login_required
def event_create_view(request, ad_index):
    if request.method == "GET":
        form = new_Event()
        return render(request, 'CYO/create.html', {
            "form": form,
            "type": "Create an event"
        })
    if request.method == "POST":
        event = new_Event(request.POST)
        adventure = Adventure.objects.get(id = ad_index)
        if event.is_valid and adventure.user == request.user :
            event = event.save(commit = False)
            event.adventure = Adventure.objects.get(id = ad_index)
            event.save()
            return HttpResponseRedirect(reverse('ev_edit', kwargs = {'index': event.id}))
        elif not event.is_valid:
            return render(request, 'CYO/create.html', {
                "type": "Create an event",
                "form": event,
                "message": "Faulty form"
            })
        else:
            return render(request, 'CYO/create.html', {
                "form": event,
                "type": "Create an event",
                "message": "Only the adventure creator may add events"
            })

@login_required
def event_edit_view(request, index):
    if request.method == "GET":
        try:
            event = Event.objects.get(id = index)
        except Event.DoesNotExist:
            return render(request, 'layout.html', {
                "message": "No such event"
            })
        if event.adventure.user == request.user:
            return render(request, 'CYO/edit.html', {
                "event": event
            })
        else:
            return render(request, 'CYO/layout.html', {
                "message": "Only the creator may view this"
            })

@login_required
def event_item_view(request, event_index):
    if request.method == "GET":
        try:
            adventure = Event.objects.get(id = event_index).adventure
        except Event.DoesNotExist:
                return render(request, 'CYO/layout.html', {
                    "message": "No such event"
                })
        form = new_Item()
        form.fields['itemstyle'] = forms.ModelChoiceField(queryset = ItemStyle.objects.filter(adventure = adventure))
        return render(request, 'CYO/create.html', {
            "form": form,
            "type": "Add an item to the event"
        })
    if request.method == "POST":
        item = new_Item(request.POST)
        if item.is_valid:
            item = item.save(commit = False)
            try:
                event = Event.objects.get(id = event_index)
            except Event.DoesNotExist:
                return render(request, 'CYO/layout.html', {
                    "message": "No such event"
                })
            item.event = event
            item.adventure = item.event.adventure
            item.save()
            return HttpResponseRedirect(reverse('ev_edit', kwargs = {'index': event_index}))
        return render(request, 'CYO/create.html', {
            "form": item,
            "type": "Add an item to the event",
            "message": "Faulty form"
        })

# Choice creation code
@login_required
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
        if adventure.user != request.user:
            return render(request, 'CYO/create.html', {
                "type": "Create a choice",
                "form": choice,
                "message": "Only the creator of the adventure may do this"
            })
        # choice.fields['final'] = forms.ModelChoiceField(queryset = Event.objects.filter(adventure = adventure))
        if choice.is_valid:
            choice = choice.save(commit = False)
            choice.initial = Event.objects.get(id = event_index)
            choice.save()
            return HttpResponseRedirect(reverse('ev_edit', kwargs = {'index': event_index}))
        return render(request, 'CYO/create.html', {
                "type": "Create a choice",
                "form": choice,
                "message": "Faulty form"
            })

@login_required
def choice_item_view(request, choice_index):
    if request.method == "GET":
        try:
            adventure = Choice.objects.get(id = choice_index).initial.adventure
        except Choice.DoesNotExist:
                return render(request, 'CYO/layout.html', {
                    "message": "No such choice"
                })
        form = new_Item()
        form.fields['itemstyle'] = forms.ModelChoiceField(queryset = ItemStyle.objects.filter(adventure = adventure))
        return render(request, 'CYO/create.html', {
            "form": form,
            "type": "Add an item requirement to the choice"
        })
    if request.method == "POST":
        item = new_Item(request.POST)
        if item.is_valid:
            item = item.save(commit = False)
            try:
                choice = Choice.objects.get(id = choice_index)
            except Choice.DoesNotExist:
                return render(request, 'CYO/layout.html', {
                    "message": "No such choice"
                })
            item.choice = choice
            item.adventure = choice.initial.adventure
            item.save()
            return HttpResponseRedirect(reverse('ev_edit', kwargs = {'index': choice.initial.id}))
        return render(request, 'CYO/create.html', {
                "type": "Add an item requirement to the choice",
                "form": item,
                "message": "Only the creator may add these"
            })

# Main display code
@login_required
def adventure_view(request, adventure_index):
    if request.method == "GET":
        try:
            adventure = Adventure.objects.get(id = adventure_index)
        except Adventure.DoesNotExist:
            return render(request, 'CYO/layout.html',
            {
                "message": "No such adventure"
            })
        return render(request, 'CYO/adventure_view.html', 
        {
            "adventure": adventure
        })

@login_required
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
            conditions_temp = choice.Conditions.all()
            conditions = []
            for condition in conditions_temp:
                conditions.append(condition.serialize)
            choices.append([choice.final.id, choice.text, conditions])
        items_temp = event.Items.all()
        items = []
        for item in items_temp:
            items.append(item.serialize)
        return JsonResponse({
            "title": event.title,
            "text": event.text,
            "items": items,
            "choices": choices
        }, status = 200)

#Login code
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
            return render(request, "CYO/login.html",
            {
                "message": "That user does not exist"
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
            return render(request, "CYO/register.html", {
                "message": "Password and confirm did not match"
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "CYO/register.html", {
                "message": "That username is already taken"
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))

@login_required
def delete_view(request, type, index):
    if request.method == "GET":
        if type == "event":
            event = Event.objects.get(id = index)
            if event == event.adventure.startevent or event == event.adventure.endevent:
                return HttpResponseRedirect(reverse('ad_edit', kwargs = {'index': event.adventure.id}))
        return render(request, 'CYO/delete.html', {
            "type": type,
            "index": index,
        })

@login_required
def generic_edit(request, type, index):
    if request.method == "POST" and request.POST.get('delete', None) is not None:
        delete = True
    else:
        delete = False
    if type == "adventure":
        try:
            instance = Adventure.objects.get(id = index)
        except Adventure.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))
        user = instance.user
        if request.method == "POST":
            if not delete:
                object = new_Adventure(request.POST, instance = instance)
                path = 'ad_edit'
                args = instance.id
            else:
                path = 'index'
                args = ''
        elif request.method == "GET":
            form = new_Adventure(instance = instance)
    elif type == "event":
        try:
            instance = Event.objects.get(id = index)
        except Event.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))
        user = instance.adventure.user
        if request.method == "POST":
            if not delete:
                object = new_Event(request.POST, instance = instance)
                path = 'ev_edit'
                args = instance.id
            else:
                path = 'ad_edit'
                args = instance.adventure.id
                if instance.adventure.startevent == instance or instance.adventure.endevent == instance:
                    return HttpResponseRedirect(reverse('ad_edit', kwargs = {'index': instance.adventure.id}))
        elif request.method == "GET":
            form = new_Event(instance = instance)
    elif type == "itemstyle":
        try:
            instance = ItemStyle.objects.get(id = index)
        except ItemStyle.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))
        user = instance.adventure.user
        if request.method == "POST":
            if not delete:
                object = new_ItemStyle(request.POST, instance = instance)
                if instance.name == "Health" and instance.type == "Status":
                    return HttpResponseRedirect(reverse('ad_edit', kwargs = {'index': instance.adventure.id}))
            path = 'ad_edit'
            args = instance.adventure.id
        elif request.method == "GET":
            form = new_ItemStyle(instance = instance)
    elif type == "choice":
        try:
            instance = Choice.objects.get(id = index)
        except Choice.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))
        user = instance.initial.adventure.user
        if request.method == "POST":
            if not delete:
                object = new_Choice(request.POST, instance = instance)
            path = 'ev_edit'
            args = instance.initial.id
        elif request.method == "GET":
            adventure = instance.initial.adventure
            form = new_Choice(instance = instance)
            form.fields['final'] = forms.ModelChoiceField(queryset = Event.objects.filter(adventure = adventure))
    elif type == "item":
        try:
            instance = Item.objects.get(id = index)
        except Item.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))
        if instance.event is not None:
            adventure = instance.event.adventure
            args = instance.event.id
        elif instance.choice is not None:
            adventure = instance.choice.initial.adventure
            args = instance.choice.initial.id
        user = adventure.user
        if request.method == "POST":
            if not delete:
                object = new_Item(request.POST, instance = instance)
            path = 'ev_edit'
        elif request.method == "GET":
            form = new_Item(instance = instance)
            form.fields['itemstyle'] = forms.ModelChoiceField(queryset = ItemStyle.objects.filter(adventure = adventure))
    else:
        return render(request, 'CYO/index.html', {
            "message": "Invalid type passed to edit"
        })
    if request.method == "GET":
        if user == request.user:
            return render(request, 'CYO/create.html', {
                "type": "Edit " + type,
                "form": form
            })
        else:
            return render(request, 'CYO/create.html', {
                "type": "Edit " + type,
                "message": "Only the creator of the adventure may edit the adventure and its components"
            })
    if request.method == "POST":
        if user == request.user:
            if delete:
                instance.delete()
                return HttpResponseRedirect(reverse(path, args = str(args)))
            if object.is_valid:
                object.save()
                return HttpResponseRedirect(reverse(path, kwargs= { 'index': args}))
            else:
                return render(request, 'CYO/create.html', {
                    "type": "Edit " + type,
                    "form": object,
                    "message": "Invalid form, please fix"
                })
        else:
            return render(request, 'CYO/create.html', {
                    "form": object,
                    "type": "Edit" + type,
                    "message": "Only the creator of the adventure may edit the adventure and its components"
                })