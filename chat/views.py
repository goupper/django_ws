# coding: utf-8
import random

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout, authenticate

from .models import *


@login_required(login_url='/login/')
def chat(request, label=None):
    room = Room.objects.filter(
        label=label, is_delete=False
    )
    if room.exists():
        room = room.first()
    else:
        room = Room.objects.filter(is_delete=False).first()

    messages = Message.objects.filter(
       room=room
    ).order_by('send_time')
    users = RoomUser.objects.filter(
        room=room, is_delete=False
    ).order_by('-create_time')
    # todo 此处会有问题, 由于先建立http连接再建立websocket, 所以刷新会导致查询出来的在线用户数量不正确
    rooms = Room.objects.filter(
        is_delete=False
    )
    return render(
        request, 'chat/index.html',
        context={
            'label': room.label, 'room': room, 'messages': messages,
            'users': users, 'rooms': rooms
        })


@login_required(login_url='/login/')
def rooms(request):
    room = Room.objects.filter(
        is_delete=False
    )
    return render(request, 'chat/rooms.html', context={'rooms': room})


@login_required(login_url='/login/')
def quit(request):
    room_label = request.GET.get('room_label', '')
    # RoomUser.objects.filter(
    #     user=request.user, room__label=room_label, is_delete=False
    # ).update(is_delete=True)
    return redirect(reverse('rooms-url'))


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    tel = f'131{random.randint(12341234, 99999999)}'
    if User.objects.filter(username=username).exists():
        user = authenticate(request, username=username, password=password)
    else:
        user = User.objects.create(
            username=username, telephone=tel
        )
        user.set_password(password)
        user.save()
    if user:
        django_login(request, user)
        return redirect(reverse('rooms-url'))
    return render(request, 'login.html')


def logout(request):
    django_logout(request)
    return redirect(reverse('index'))
