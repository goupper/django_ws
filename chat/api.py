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
from rest_framework.exceptions import PermissionDenied
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
        is_show=True
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

    def get_auth_token(self):
        auth = self.request.META.get('HTTP_ACCESS_TOKEN', '')
        return auth == 'eGluanVzaGFuZzg4OA=='

    def create(self, request, *args, **kwargs):
        if self.get_auth_token():
            return super(RoomIpViewSet, self).create(request, *args, **kwargs)
        raise PermissionDenied()

    def update(self, request, *args, **kwargs):
        if self.get_auth_token():
            return super(RoomIpViewSet, self).update(request, *args, **kwargs)
        raise PermissionDenied()

    def destroy(self, request, *args, **kwargs):
        if self.get_auth_token():
            return super(RoomIpViewSet, self).destroy(request, *args, **kwargs)
        raise PermissionDenied()

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save(update_fields=['is_delete'])


class BlackIpViewSet(viewsets.ModelViewSet):
    queryset = BlackIp.objects.order_by('-create_time')
    serializer_class = BlackIpSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    order_fields = ('create_time', 'update_time', 'start_time', 'end_time')
    search_fields = ('ip', )

    def get_auth_token(self):
        auth = self.request.META.get('HTTP_ACCESS_TOKEN', '')
        return auth == 'eGluanVzaGFuZzg4OA=='

    def create(self, request, *args, **kwargs):
        if self.get_auth_token():
            return super(BlackIpViewSet, self).create(request, *args, **kwargs)
        raise PermissionDenied()

    def update(self, request, *args, **kwargs):
        if self.get_auth_token():
            return super(BlackIpViewSet, self).update(request, *args, **kwargs)
        raise PermissionDenied()

    def destroy(self, request, *args, **kwargs):
        if self.get_auth_token():
            return super(BlackIpViewSet, self).destroy(request, *args, **kwargs)
        raise PermissionDenied()

    # def perform_destroy(self, instance):
    #     instance.is_delete = True
    #     instance.save(update_fields=['is_delete'])
