"""django_ws URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from chat import views
from django_ws.settings import MEDIA_ROOT, STATIC_ROOT


urlpatterns = [
    re_path('^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}, ),
    re_path('^static/(?P<path>.*)/$', serve, {'document_root': STATIC_ROOT}, ),
    path('admin/', admin.site.urls),
    path('', views.rooms, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('room/', views.create_room, name='create-room'),
    re_path('^chat/(?P<label>[^/]+)/$', views.chat, name='chat-url'),
    re_path('^rooms/$', views.rooms, name='rooms-url'),
    path('quit/', views.quit, name='quit-room')
]
