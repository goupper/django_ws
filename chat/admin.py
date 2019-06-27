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


admin.site.register(User)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomUser, RoomUserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserIp)
admin.site.register(RoomIp)

