#!usr/bin/env python 
# -*- coding:utf-8 _*-
"""
@author:ivan
@file: serializer.py 
@version:
@time: 2019/06/27 
@email:chongwuwy@163.com
"""
from rest_framework import serializers

from .models import *


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('user', 'room', )


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ('user', )


class RoomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomUser
        fields = '__all__'


class MessageIpSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageIp
        fields = '__all__'


class RoomIpSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomIp
        fields = '__all__'
