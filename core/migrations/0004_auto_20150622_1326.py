# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_category_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='description',
            field=models.CharField(max_length=300, default='None'),
        ),
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
            field=models.CharField(max_length=100, default='None'),
        ),
        migrations.AddField(
            model_name='video',
            name='publish_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 22, 13, 26, 37, 885160, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='thumbnail',
            field=models.CharField(max_length=200, default='None'),
        ),
        migrations.AddField(
            model_name='video',
            name='views_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='video',
            name='youtube_id',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
