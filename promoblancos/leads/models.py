from django.db import models


class Colectivo(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre


class Lead(models.Model):
    nombre = models.CharField(max_length=200)
    primer_apellido = models.CharField(max_length=200)
    segundo_apellido = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    codigo_postal = models.CharField(max_length=200)
    colectivo = models.ForeignKey(Colectivo, related_name='leads', default="Desempleo")
    acreditacion = models.FileField(upload_to="acr")
    enviado_en_csv = models.BooleanField(default=False)
    enviado_cupon = models.BooleanField(default=False)
    colectivo_validado = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email
