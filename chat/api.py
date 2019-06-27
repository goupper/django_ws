#!usr/bin/env python 
# -*- coding:utf-8 _*-
"""
@author:ivan
@file: api.py 
@version:
@time: 2019/06/27 
@email:chongwuwy@163.com
"""
from rest_framework import viewsets, mixins
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

from .serializer import *
from .models import *


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.order_by('send_time')
    serializer_class = MessageSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    order_fields = ('send_time', )
