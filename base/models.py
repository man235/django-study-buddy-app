from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)    # null=True is the flag permit null value in database
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    #participants 
    updated = models.DateTimeField(auto_now=True)
    
    # set at first save and never change for mutiple save
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return str(self.name)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # delete all messages of that User
    room = models.ForeignKey(Room, on_delete=models.CASCADE)    # delete all messages in that room
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body[0:50]