#!usr/bin/env python 
# -*- coding:utf-8 _*-
"""
@author:ivan
@file: forms.py 
@version:
@time: 2019/06/26 
@email:chongwuwy@163.com
"""
from django import forms

from .models import Room


class RoomForm(forms.Form):
    name = forms.CharField(
        max_length=64, required=True
    )
    content = forms.CharField(
        max_length=128, required=False
    )
