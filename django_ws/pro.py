#!usr/bin/env python 
# -*- coding:utf-8 _*-
"""
@author:ivan
@file: pro.py 
@version:
@time: 2019/06/26 
@email:chongwuwy@163.com
"""
from .settings import *


DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # 'django.db.backends.postgresql',
        'NAME': 'django_ws',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5433',
        'ATOMIC_REQUESTS': True,
    }
}
