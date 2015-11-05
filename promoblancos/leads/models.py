from django.db import models


class Lead(models.Model):
    nombre = models.CharField(max_length=200)
    primer_apellido = models.CharField(max_length=200)
    segundo_apellido = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    codigo_postal = models.CharField(max_length=200)

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email
