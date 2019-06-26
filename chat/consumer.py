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

            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # 从房间移除用户
        await self.group_remove_user()

    @database_sync_to_async
    def send_message(self, content=''):
        room = Room.objects.filter(
            label=self.scope.get('url_route')['kwargs']['room_name']
        ).first()
        message = Message.objects.create(
            room=room, content=content, user=self.get_user()
        )
        self.message_user_id = message.user_id
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
            )
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
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        owner_str = '(房主)' if event['message']['user']['id'] == self.room_owner_id else ''
        if event['message']['user']['id'] == self.login_user_id:
            message = f'{now}  我{owner_str}：' + event['message']['message']['content']
        else:
            message = f'{now}  {event["message"]["user"]["username"]}{owner_str}：' + event['message']['message']['content']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

