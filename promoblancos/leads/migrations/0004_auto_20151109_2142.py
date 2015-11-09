# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0003_auto_20151109_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='codigo_cupon',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'Creado'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name=b'Actualizado'),
        ),
    ]
