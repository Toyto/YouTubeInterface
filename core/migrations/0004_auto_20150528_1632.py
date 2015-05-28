# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_category_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='youtube_id',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
