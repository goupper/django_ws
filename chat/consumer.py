#!usr/bin/env python 
# -*- coding:utf-8 _*-
"""
@author:ivan
@file: consumer.py 
@version:
@time: 2019/06/25 
@email:chongwuwy@163.com
"""
import json
import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.forms.models import model_to_dict
from django.core.cache import cache

from .models import *


# todo 1. 广播消息 2. 单人私聊
class ChatConsumer(AsyncWebsocketConsumer):
    room_group_name = None
    room_owner_id = None
    login_user_id = None
    # group_send 时会出现问题(message_user_id不正确), 不能使用
    # message_user_id = None

    def is_room_owner(self, message_user_id):
        # 当前登录用户是否是房主
        return message_user_id == self.room_owner_id

    def get_user(self):
        self.login_user_id = self.scope['user'].id
        return self.scope['user']

    @database_sync_to_async
    def group_add_user(self, room):
        # 用户加入房间
        user = self.get_user()
        # is_owner 是否是房主
        is_owner = user.id == room.get('id')
        room_user = RoomUser.objects.filter(
            user=user, room_id=room.get('id')
        )
        if room_user.exists():
            # 重新加入房间
            room_user.update(is_delete=False)
        else:
            # 第一次加入房间
            RoomUser.objects.create(
                user=user, room_id=room.pop('id'), is_delete=False, is_owner=is_owner
            )

    @database_sync_to_async
    def group_remove_user(self):
        # 将用户移除房间
        user = self.get_user()
        RoomUser.objects.filter(
            user=user, room__label=self.scope.get('url_route')['kwargs']['room_name']
        ).update(is_delete=True)

    @database_sync_to_async
    def get_room(self):
        # 查询房间是否存在
        room = Room.objects.filter(
            label=self.scope.get('url_route')['kwargs']['room_name'])
        if room.exists():
            room = room.values().first()
            self.room_owner_id = room['user_id']
            return room

    @database_sync_to_async
    def online_user_count(self):
        # 统计在线用户
        room_user_count = RoomUser.objects.filter(
            is_delete=False, room__label=self.scope.get('url_route')['kwargs']['room_name']
        ).count()
        return room_user_count

    def get_now_time(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    async def user_connect_or_disconnect_notify(self, notify='connect'):
        # 用户进入/离开 广播通知
        connect_user = self.get_user()
        online_user_count = await self.online_user_count()
        content = f'用户{connect_user.username}进入了房间({online_user_count}人在线)' if notify == 'connect' \
            else f'用户{connect_user.username}离开了房间({online_user_count}人在线)'
        rs = dict(
            user=dict(
                id=connect_user.id, username=connect_user.username
            ),
            message=dict(
                id=1, content=content, room_id=self.room_group_name
            ),
            notify=True
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': rs
            }
        )

    async def connect(self):
        room = await self.get_room()

        # Join room group
        if room:
            self.room_group_name = room.get('label')
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.group_add_user(room)
            await self.user_connect_or_disconnect_notify()
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # 从房间移除用户
        await self.group_remove_user()
        await self.user_connect_or_disconnect_notify(notify='disconnect')

    @database_sync_to_async
    def send_message(self, content=''):
        room = Room.objects.filter(
            label=self.scope.get('url_route')['kwargs']['room_name']
        ).first()
        message = Message.objects.create(
            room=room, content=content, user=self.get_user()
        )
        return message

    # Receive message from WebSocket
    async def receive(self, text_data=None):
        # 收到消息后, 再把消息转发到对应的房间(广播消息)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message = await self.send_message(message)

        rs = dict(
            user=dict(
                id=message.user.id, username=message.user.username
            ),
            message=dict(
                id=message.id, content=message.content, room_id=message.room_id
            ),
            notify=False
        )
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': rs
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # 会for循环将消息依次发送给房间内的所有用户
        now = self.get_now_time()
        if not event['message']['notify']:
            owner_str = '(房主)' if event['message']['user']['id'] == self.room_owner_id else ''
            if event['message']['user']['id'] == self.login_user_id:
                message = f'{now}  我{owner_str}：' + event['message']['message']['content']
            else:
                message = f'{now}  {event["message"]["user"]["username"]}{owner_str}：' + \
                          event['message']['message']['content']
        else:
            message = f'{now}  系统通知：' + event['message']['message']['content']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def notify_message(self, event):
        # 系统广播通知
        now = self.get_now_time()
        message = f"{now} : {event['message']['message']}"
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class RoomConsumer(AsyncWebsocketConsumer):
    room_owner_id = 1
    room_group_name = None
    room_id = None

    @database_sync_to_async
    def get_room(self):
        # 查询房间是否存在
        room = RoomIp.objects.filter(
            label=self.scope.get('url_route')['kwargs']['room_name'], is_delete=False)
        if room.exists():
            room = room.values().first()
            return room
        return RoomIp.objects.filter(
            is_delete=False
        ).values().first()

    @database_sync_to_async
    def add_user(self, request):
        # 用户进入房间记录
        ip = self.get_user_ip(request)
        user_ip = UserIp.objects.create(
            ip=ip
        )
        return user_ip

    async def user_connect_or_disconnect_notify(self, notify_type='connect'):
        # 用户进入/离开房间通知
        user_ip = self.get_user_ip()
        now = self.get_now_time()
        # 更新在线用户人数
        room_user_number = self.room_user_number(number_type=notify_type)

        notify_content = '进入' if notify_type == 'connect' else '离开'
        message = f'{now} 系统通知 : {user_ip}{notify_content}了房间({room_user_number}人在线)'
        rs = dict(
            message=message,
            notify=False
        )
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notify_message',
                'message': rs
            }
        )

    def get_user_ip(self):
        # 获取用户ip
        request = self.scope['request']
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')
        if x_forwarded_for and x_forwarded_for[0]:
            login_ip = x_forwarded_for[0]
        else:
            login_ip = request.META.get('REMOTE_ADDR', '')
        return login_ip

    def room_user_number(self, number_type='connect'):
        # 更新在线用户人数
        # todo user aioredis
        cache_key = f'room:{self.room_id}'
        room_user_number = cache.get(cache_key, 0)
        if number_type == 'connect':
            room_user_number += 1
        else:
            room_user_number -= 1
        cache.set(cache_key, room_user_number)
        return room_user_number

    def get_now_time(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    async def connect(self):
        room = await self.get_room()
        # Join room group
        if room:
            self.room_group_name = room.get('label')
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.add_user(self.scope['request'])
            await self.user_connect_or_disconnect_notify()
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # 从房间移除用户
        await self.user_connect_or_disconnect_notify(notify_type='disconnect')

    # Receive message from WebSocket
    async def receive(self, text_data=None):
        # 收到消息后, 再把消息转发到对应的房间(广播消息)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        rs = dict(
            message=message,
            notify=False
        )
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': rs
            }
        )

    async def notify_message(self, event):
        # 系统广播通知
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message']['message']
        }))

    async def chat_message(self, event):
        # 消息发送
        now = self.get_now_time()
        user_ip = self.get_user_ip()
        message = f"{now} {user_ip} : {event['message']['message']}"
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

