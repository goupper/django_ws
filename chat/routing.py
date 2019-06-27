#!usr/bin/env python 
# -*- coding:utf-8 _*-
"""
@author:ivan
@file: router.py 
@version:
@time: 2019/06/25 
@email:chongwuwy@163.com
"""
from django.conf.urls import re_path

from . import consumer


websocket_urlpatterns = [
    # re_path(r'^ws/chat/$', consumer.ChatConsumer),
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', consumer.ChatConsumer),
    re_path(r'^ws/room/(?P<room_name>[^/]+)/$', consumer.RoomConsumer),
]
