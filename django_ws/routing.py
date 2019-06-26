#!usr/bin/env python 
# -*- coding:utf-8 _*-
"""
@author:ivan
@file: routing.py 
@version:
@time: 2019/06/25 
@email:chongwuwy@163.com
"""
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
