from django.apps import AppConfig


class ChatConfig(AppConfig):
    name = 'chat'

    def ready(self):
        from chat.models import RoomUser, RoomUserIp
        # 重启服务器时, 更新所有客户端为离线状态
        RoomUserIp.objects.all().update(is_online=False)
        RoomUser.objects.all().update(is_delete=False)

