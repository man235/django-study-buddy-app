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
from .models import Room, Topic, models
from .form import RoomForm


# must the same quotation marks between key-name and value
# rooms = [ 
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Backend Developer'}
# ]


def loginPage(request):
    page = 'login'

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

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

    topics = Topic.objects.all()

    # get room count
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}

    return render(request, 'base/home.html', context)



def room(request, pk):
    room = Room.objects.get(id=str(pk))
    context = {'room': room}

    return render(request, 'base/room.html', context)


# restrice user
@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save() # save to the database
            return redirect(home)

    context = {'form': form}

    return render(request, 'base/room_form.html', context)



@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)  # passing the above room

    # validate host and users of this room
    if request.user != room.host:
        return HttpResponse('Yout are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect(home)

    context = {'form': form}

    return render(request, 'base/room_form.html', context)



@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}

    return render(request, 'base/delete.html', context)