# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150610_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='description',
            field=models.CharField(default='None', max_length=300),
        ),
    ]
