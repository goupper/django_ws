# Generated by Django 2.2.2 on 2019-06-27 14:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20190627_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomuserip',
            name='last_connect_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='last_connect_time'),
            preserve_default=False,
        ),
    ]