# Generated by Django 2.2.2 on 2019-07-01 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_auto_20190701_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='messageip',
            name='is_notify',
            field=models.BooleanField(blank=True, default=False, verbose_name='is_notify'),
        ),
        migrations.AlterField(
            model_name='messageip',
            name='is_show',
            field=models.BooleanField(blank=True, default=True, verbose_name='is_show'),
        ),
    ]
