# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Colectivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('primer_apellido', models.CharField(max_length=200)),
                ('segundo_apellido', models.CharField(max_length=200)),
                ('email', models.CharField(unique=True, max_length=200)),
                ('codigo_postal', models.CharField(max_length=200)),
                ('acreditacion', models.FileField(upload_to=b'acreditaciones')),
                ('enviado_en_csv', models.BooleanField(default=False)),
                ('enviado_cupon', models.BooleanField(default=False)),
                ('colectivo_validado', models.BooleanField(default=False)),
                ('colectivo', models.ForeignKey(related_name='leads', to='leads.Colectivo')),
            ],
        ),
    ]
