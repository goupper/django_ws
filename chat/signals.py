#!usr/bin/env python 
# -*- coding:utf-8 _*-
"""
@author:ivan
@file: signals.py 
@version:
@time: 2019/07/01 
@email:chongwuwy@163.com
"""
import typing
import datetime
import logging

from django.dispatch import Signal
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

from .models import BlackIp, MessageIp, UserIp


logger = logging.getLogger(__name__)


@receiver(post_save, sender=BlackIp)
def receive_insert_black_user(
        sender: typing.Any,
        instance: typing.Any,
        **kwargs
) -> typing.Any:
    """
    notify black user message
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    if kwargs.get('created', False):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        MessageIp.objects.create(
            room_id=1, user_id=UserIp.objects.filter(ip=instance.ip).first().id,
            content=f'{now} 系统通知 : {instance.ip} 违规已经被禁用!',
            is_notify=True, send_time=now
        )
