# -*- coding: utf-8 -*-
from django.db import models
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


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
    email = models.EmailField(max_length=200, unique=True, error_messages={'unique': "Ya existe un Registro con este Email."})
    codigo_postal = models.CharField(max_length=200)
    colectivo = models.ForeignKey(Colectivo, related_name='leads')
    acreditacion = models.FileField(upload_to="acr", verbose_name='Certificación de pertenencia al colectivo')
    colectivo_validado = models.BooleanField(default=False)
    enviado_en_csv = models.BooleanField(default=False)
    enviado_cupon = models.BooleanField(default=False)
    codigo_cupon = models.CharField(null=True, blank=True, max_length=200)

    class META:
        verbose_name = "Registro"

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email

    def enviar_email_inicial(self):
        mail = EmailMultiAlternatives(
            subject="Confirmación registro Juguetes Blancos",
            body='Hola  Jesús, Gracias por registrarte en Juguetes Blancos. Hemos recibido tu solicitud del cupón de 10€ para la compra de juguetes y bicicletas en Hipercor. Una vez hayamos comprobado que tu documentación es correcta, te enviaremos el cupón  nominativo dentro de un plazo de 5 días. ¡Hasta muy pronto! Rocío Leiva Trabajadora Social y Asesora de Usuari@s Beneficiarios en Tarifas Blancas Habla de Juguetes Blancos a tus amig@s :)',
            from_email="Rocio, JueguetesBlancos <rocioleiva@tarifasblancas.com>",
            to=[self.email]
        )
        mail.attach_alternative(render_to_string('leads/email_inicial.html', {'lead': self}), "text/html")
        mail.send()
