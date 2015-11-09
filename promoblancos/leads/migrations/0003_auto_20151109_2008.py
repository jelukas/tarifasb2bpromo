# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_auto_20151108_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 20, 7, 59, 798280, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 20, 8, 18, 452335, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lead',
            name='acreditacion',
            field=models.FileField(upload_to=b'acr'),
        ),
    ]
