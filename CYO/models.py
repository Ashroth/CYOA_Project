from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Choice(models.Model):
    initial = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="Start")
    final = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="End")
    condition_amount = models.IntegerField(default=0)
    text = models.TextField()

class Event(models.Model):
    adventure = models.ForeignKey("Adventure", on_delete=models.CASCADE, related_name="Events")
    text = models.TextField()
    title = models.TextField(max_length=255)
    def __str__(self):
        return '%s' %self.title

class Adventure(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="Creations")
    title = models.TextField(max_length=255)
    description = models.TextField()
    startevent = models.ForeignKey("Event", on_delete=models.SET_NULL, null=True, related_name="First_screen")
    endevent = models.ForeignKey("Event", on_delete=models.SET_NULL, null=True, related_name="End_screen")

class Item(models.Model):
    status = 'Stat'
    item = 'Item'
    hidden_trigger = 'hidden'
    initialization = 'Init'
    ITEM_TYPE_CHOICES = [
        (status, 'Status'),
        (item, 'Item'),
        (hidden_trigger, 'Hidden_Trigger'),
        (initialization, 'Initialization')
    ]
    name = models.TextField(max_length=64)
    type = models.CharField(choices = ITEM_TYPE_CHOICES, default = status)
    amount = models.IntegerField()
