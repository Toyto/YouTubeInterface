# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150528_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='dislikes_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='likes_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='name',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='video',
            name='ratio',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='thumbnail',
            field=models.CharField(default='None', max_length=200),
        ),
        migrations.AddField(
            model_name='video',
            name='views_count',
            field=models.IntegerField(default=0),
        ),
    ]
