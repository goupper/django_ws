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
    ip = serializers.SerializerMethodField()

    def get_ip(self, obj):
        return UserIp.objects.filter(
            id=obj.user_id
        ).first().ip

    class Meta:
        model = MessageIp
        exclude = ('user_id', )


class RoomIpSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomIp
        fields = '__all__'


class BlackIpSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlackIp
        fields = '__all__'
