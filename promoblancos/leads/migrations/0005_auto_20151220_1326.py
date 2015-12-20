# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0004_auto_20151109_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='acreditacion',
            field=models.FileField(upload_to=b'acr', null=True, verbose_name=b'Certificaci\xc3\xb3n de pertenencia al colectivo', blank=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='email',
            field=models.EmailField(unique=True, max_length=200, error_messages={b'unique': b'Ya existe un Registro con este Email.'}),
        ),
    ]
