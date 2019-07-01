#!usr/bin/env python 
# -*- coding:utf-8 _*-
"""
@author:ivan
@file: api.py 
@version:
@time: 2019/06/27 
@email:chongwuwy@163.com
"""
from rest_framework import viewsets, HTTP_HEADER_ENCODING
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from rest_framework import status
from rest_framework.decorators import (action, )
from rest_framework.throttling import ScopedRateThrottle, AnonRateThrottle, UserRateThrottle
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from django.core.cache import cache
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.utils.six import text_type

from .serializer import *
from .models import *
from .utils import CustomPageNumberPagination


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.order_by('send_time')
    serializer_class = MessageSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    order_fields = ('send_time', )


class MessageIpViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MessageIp.objects.filter(
        is_show=False
    ).order_by('-send_time')
    serializer_class = MessageIpSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    order_fields = ('send_time', 'user_id')
    search_fields = ('user_id', 'room_id')
    pagination_class = CustomPageNumberPagination


class RoomIpViewSet(viewsets.ModelViewSet):
    queryset = RoomIp.objects.filter(
        is_delete=False
    ).order_by('-create_time')
    serializer_class = RoomIpSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    order_fields = ('create_time', )
    search_fields = ('label', 'name', 'content')
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'destroy']:
            auth = self.request.META.get('ACCESS-TOKEN', b'')
            if isinstance(auth, text_type):
                # Work around django test client oddness
                auth = auth.encode(HTTP_HEADER_ENCODING)
            if auth != 'xinjushang888':
                return Response(status.HTTP_403_FORBIDDEN)
        return super(RoomIpViewSet, self).get_serializer_class()
