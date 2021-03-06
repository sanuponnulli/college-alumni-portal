from atexit import register
from email import message
from importlib.metadata import requires
from os import name
from django.http import HttpResponse
from multiprocessing import context
from pydoc_data.topics import topics
from pyexpat import model
from telnetlib import AUTHENTICATION
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from . models import Room,Topic,Message,User,Report
from .forms import RoomForm,UserForm,MyUserCreationForm
from django.db.models import Q

from django.contrib.auth import authenticate,login,logout
from django.contrib import messages





# Create your views here.
def loginpage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email=request.POST.get('email').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request,'user does not exist')
        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username OR Password Missing!')    
        
    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')
def registerPage(request):
    form=MyUserCreationForm()
    if request.method=='POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'an error occured during registration')    
    return render(request,'base/login_register.html',{'form':form})

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''

    rooms=Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )
    topics=Topic.objects.all()[0:5]
    room_count=rooms.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)
@login_required(login_url='login')
def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topic=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topic}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,craeted=Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        # form=RoomForm(request.POST)
        # if form.is_valid():
        #     room=form.save(commit=False)
        #     room.host=request.user
        #     room.save()
        return redirect('home')

    context={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)
@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('you are not allowed here')

    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,craeted=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.save()
        room.description=request.POST.get('description')
        
        return redirect('home')
    context={'form':form,'topic':topics,'room':room}
    return render(request,'base/room_form.html',context)

def report(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    participants=room.participants.all()
    if request.user not in participants:
        return HttpResponse('you are not allowed here')

    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,craeted=Topic.objects.get_or_create(name=topic_name)
        Report.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        
        return redirect('home')
    context={'form':form,'topic':topics,'room':room}
    return render(request,'base/report.html',context)


@login_required(login_url='login')    
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('you are not allowed here')
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')    
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('you are not allowed here')
    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message}) 


@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method=='POST':
        form=UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-Profile',pk=user.id)
    return render (request,'base/update_user.html',{'form':form} )


def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    topic=Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topic':topic})

def activityPage(request):
    room_messages=Message.objects.all()
    return render(request,'base/activity.html',{'room_messages':room_messages})


    