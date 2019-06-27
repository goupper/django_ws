import os

import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_ws.settings")
django.setup()
application = get_default_application()

from chat.models import RoomUserIp, RoomUser


# 重启服务器时, 更新所有客户端为离线状态
RoomUserIp.objects.all().update(is_online=False)
RoomUser.objects.all().update(is_delete=False)
