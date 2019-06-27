# coding: utf-8
from django.contrib import admin

from .models import *


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'user')
    list_per_page = 20
    list_filter = ('name', )


class RoomUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'is_delete', 'is_owner')
    list_per_page = 20
    list_filter = ('user', 'room', 'is_delete', 'is_owner')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'send_time')
    list_per_page = 20


class RoomUserIpAdmin(admin.ModelAdmin):
    list_display = (
        'ip', 'room_ip_id', 'client_port', 'is_online',
        'connect_time', 'disconnect_time', 'last_connect_time'
    )
    list_filter = ('is_online', 'room_ip_id')
    list_per_page = 20
    search_fields = ('ip', )


class UserIpAdmin(admin.ModelAdmin):
    list_display = ('ip', 'username')
    list_per_page = 20
    search_fields = ('ip', 'username')


class RoomIpAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'content')
    list_per_page = 20
    list_filter = ('name',)
    search_fields = ('name', 'label')


admin.site.register(User)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomUser, RoomUserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserIp, UserIpAdmin)
admin.site.register(RoomIp, RoomIpAdmin)
admin.site.register(RoomUserIp, RoomUserIpAdmin)
