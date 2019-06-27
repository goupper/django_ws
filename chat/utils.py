#!usr/bin/env python 
# -*- coding:utf-8 _*-
"""
@author:ivan
@file: utils.py 
@version:
@time: 2019/06/27 
@email:chongwuwy@163.com
"""
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    #: 分页处理函数
    page_size_query_param = 'size'
    page_size = 20
