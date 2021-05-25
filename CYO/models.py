from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Choice(models.Model):
    initial = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="Start")
    final = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="End")
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
    startevent = models.ForeignKey("Event", on_delete=models.CASCADE, null=True, related_name="First_screen")
    endevent = models.ForeignKey("Event", on_delete=models.SET_NULL, null=True, related_name="End_screen")

class ItemStyle(models.Model):
    status = 'Status'
    item = 'Item'
    hidden_trigger = 'Hidden'
    ITEM_TYPE_CHOICES = [
        (status, 'Status'),
        (item, 'Item'),
        (hidden_trigger, 'Hidden Trigger')
    ]
    name = models.TextField(max_length=64)
    type = models.CharField(choices = ITEM_TYPE_CHOICES, default = status, max_length=64)
    adventure = models.ForeignKey("Adventure", on_delete=models.CASCADE, null=True, related_name="All_Items")
    def __str__(this):
        return this.name


class Item(models.Model):
    itemstyle = models.ForeignKey("ItemStyle", on_delete=models.CASCADE, related_name="Instances")
    hidden = models.BooleanField(default = False)
    amount = models.IntegerField()
    event = models.ForeignKey("Event", on_delete=models.CASCADE, null=True, related_name="Items")
    choice = models.ForeignKey("Choice", on_delete=models.CASCADE, null=True, related_name="Conditions")

    @property
    def serialize(self):
        return {
            "name": self.itemstyle.name,
            "type": self.itemstyle.type,
            "hidden": self.hidden,
            "amount": self.amount
        }