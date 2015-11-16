# -*- coding: utf-8 -*-
from django.db import models


class Colectivo(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre


class Lead(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Actualizado')
    nombre = models.CharField(max_length=200)
    primer_apellido = models.CharField(max_length=200)
    segundo_apellido = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    codigo_postal = models.CharField(max_length=200)
    colectivo = models.ForeignKey(Colectivo, related_name='leads', default="Desempleo")
    acreditacion = models.FileField(upload_to="acr", verbose_name='Certificación de pertenencia al colectivo')
    colectivo_validado = models.BooleanField(default=False)
    enviado_en_csv = models.BooleanField(default=False)
    enviado_cupon = models.BooleanField(default=False)
    codigo_cupon = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email
