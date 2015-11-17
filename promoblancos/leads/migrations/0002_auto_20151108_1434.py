# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='acreditacion',
            field=models.FileField(upload_to=b''),
        ),
        migrations.AlterField(
            model_name='lead',
            name='colectivo',
            field=models.ForeignKey(related_name='leads', to='leads.Colectivo'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='email',
            field=models.EmailField(unique=True, max_length=200),
        ),
    ]
