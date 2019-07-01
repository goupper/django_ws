# Generated by Django 2.2.2 on 2019-07-01 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20190701_0858'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messageip',
            options={'verbose_name': 'MessageIp', 'verbose_name_plural': 'MessageIp'},
        ),
        migrations.AddField(
            model_name='roomuserip',
            name='disconnect_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, ''), (1, '用户断开'), (2, '系统重启'), (3, '连接超时'), (4, '违规被踢')], default=0),
        ),
        migrations.AddIndex(
            model_name='roomuserip',
            index=models.Index(fields=['disconnect_type'], name='chat_roomus_disconn_100853_idx'),
        ),
    ]