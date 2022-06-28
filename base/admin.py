from django.contrib import admin

# Register your models here.

from .models import Message, Room, Topic

""" Create all below tables in admin panel """
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
