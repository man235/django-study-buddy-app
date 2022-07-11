import re
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required   # use to restrict user access
from django.db.models import Q
from django.contrib.messages import constants as messages
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, models, Message
from .form import RoomForm, UserForm



def loginPage(request):
    page = 'login'

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, 
                            username=username,
                            password=password)

        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Username of password does not exist')

    context = {'page': page}

    return render(request, 'base/login_register.html', context)



def logoutUser(request):
    logout(request)
    
    return redirect('home')



def registerPage(request):
    # page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # commit=False : return a object haven't exist in database yet
            # this creates, but don't save the new form instance
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            login(request, user)

            return redirect('home')
        else:
            messages.error(request, 'An eror occurred during registration')

    context = {'form': form}

    return render(request, 'base/login_register.html', context)



# Perform home page
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''    # equal to paramter passed into the url

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)       
    ) 
    
    # limit 5 displayed topics in home page
    topics = Topic.objects.all()[0:5]

    # count rooms
    room_count = rooms.count()

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,
                'room_messages': room_messages}

    return render(request, 'base/home.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()   # get messages that correspond to the user owner 
    topics = Topic.objects.all

    context = {'rooms': rooms, 'user': user,
               'room_messages': room_messages, 'topics': topics}
    
    return render(request, 'base/profile.html', context)



def room(request, pk):
    room = Room.objects.get(id=str(pk))

    room_messages = room.message_set.all().order_by('-created')     # orderd by newest created date

    participants = room.participants.all()    

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'),
        )
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
                'participants': participants}

    return render(request, 'base/room.html', context)



# restrict user access
@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm() 
    topics = Topic.objects.all()

    if request.method == 'POST':
        # get the topic field's name
        topic_name = request.POST.get('topic')

        # define the new topic or it existed
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
            
        return redirect(home)

    context = {'form': form, 'topics': topics}

    return render(request, 'base/room_form.html', context)



@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)  # passing the above room instance to the form
    topics = Topic.objects.all()

    # validate the host and users of this room
    if request.user != room.host:
        return HttpResponse('Yout are not allowed here!!')

    if request.method == 'POST':
        # get the topic field's name
        topic_name = request.POST.get('topic')
        # define the new topic or it existed
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')

        room.save()

        return redirect(home)

    context = {'form': form, 'topics': topics, 'room': room}

    return render(request, 'base/room_form.html', context)



@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('Yout are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}

    return render(request, 'base/delete.html', context)



@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('Yout are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
        
    context = {'obj': message}

    return render(request, 'base/delete.html', context)



@login_required(login_url='login')
def updateUser(request):
    user = request.user

    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form': form}

    return render(request, 'base/update_user.html', context)



def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''    # equal to paramter passed into the url

    topics = Topic.objects.filter(name__icontains=q)

    context = {'topics': topics}
    return render(request, 'base/topics.html', context)

