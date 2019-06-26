#!usr/bin/env python 
# -*- coding:utf-8 _*-
"""
@author:ivan
@file: asgi.py 
@version:
@time: 2019/06/26 
@email:chongwuwy@163.com
"""
"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_ws.pro")
django.setup()
application = get_default_application()
