# -*- coding: utf-8 -*-
import sendgrid
from unipath import Path
import fnmatch
import os

from django.core.mail import EmailMultiAlternatives
from django.contrib import admin
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from daterange_filter.filter import DateRangeFilter

from .models import Lead, Colectivo


def marcar_enviado_en_csv(modeladmin, request, queryset):
    queryset.update(enviado_en_csv=True)
marcar_enviado_en_csv.short_description = "Marcar como Enviado en CSV"


def marcar_cupon_enviado(modeladmin, request, queryset):
    queryset.update(enviado_cupon=True)
marcar_cupon_enviado.short_description = "Marcar como Cupon Enviado"


def marcar_colectivo_validado(modeladmin, request, queryset):
    queryset.update(colectivo_validado=True)
marcar_colectivo_validado.short_description = "Marcar como Colectivo Validado"


def marcar_colectivo_no_validado(modeladmin, request, queryset):
    queryset.update(colectivo_validado=False)
marcar_colectivo_no_validado.short_description = "Marcar como Colectivo NO Validado"


def enviar_email_con_cupon(modeladmin, request, queryset):
    leads_incorrectos = 0
    leads_correctos = 0
    for lead in queryset:
        if lead.enviado_en_csv is True and lead.enviado_cupon is False and lead.colectivo_validado is True:
            for fichero in os.listdir(settings.COUPONS_ROOT):
                if fnmatch.fnmatch(fichero, str(lead.id)+'_*.pdf'):
                    cupon_fichero = Path(settings.COUPONS_ROOT, fichero)
                    if cupon_fichero.exists():
                        codigo = fichero.split("_")[1].split(".")[0]
                        url_cupon = settings.BASE_URL+'/static/coupons/'+fichero
                        mail = EmailMultiAlternatives(
                            subject="Mi cupón de 10€ de Juguetes Blancos",
                            body='Descarga tu cupon aqui: '+url_cupon+' </p>',
                            from_email="Rocio, JueguetesBlancos <rocioleiva@tarifasblancas.com>",
                            to=[lead.email]
                        )
                        mail.attach_alternative(render_to_string('leads/email_cupon.html', {'lead': lead, 'url_cupon': url_cupon}), "text/html")
                        mail.send()
                        lead.enviado_cupon = True
                        lead.codigo_cupon = codigo
                        lead.save()
                        leads_correctos = leads_correctos+1
        else:
            leads_incorrectos = leads_incorrectos+1
    messages.success(request, str(leads_correctos)+' Email/s enviado Correctamente')
    messages.error(request, str(leads_incorrectos)+' Leads no cumplian las condiciones.')
enviar_email_con_cupon.short_description = "ENVIAR CUPON POR EMAIL"


def enviar_email_acreditacion_no_valida(modeladmin, request, queryset):
    sg = sendgrid.SendGridClient(settings.SENDGRID_API_KEY)
    message = sendgrid.Mail()
    message.set_subject('Acreditación no válida Juguetes Blancos')
    message.set_html(render_to_string('leads/email_acreditacion_no_valida.html', {}))
    message.set_from('Rocio, JueguetesBlancos <rocioleiva@tarifasblancas.com>')
    recipients = queryset.values_list("email")
    message.smtpapi.set_tos([item[0] for item in recipients])
    status, msg = sg.send(message)
    messages.success(request, 'Email enviado Correctamente.')
enviar_email_acreditacion_no_valida.short_description = "ENVIAR EMAIL: Acreditacion No Valida"


class LeadResource(resources.ModelResource):

    class Meta:
        model = Lead
        list_display = ['id', 'nombre', 'primer_apellido', 'segundo_apellido', 'email', 'codigo_postal', 'enviado_en_csv', 'enviado_cupon', 'colectivo', 'colectivo_validado', 'codigo_cupon']


class LeadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre', 'primer_apellido', 'segundo_apellido', 'email', ]
    list_filter = ['colectivo', 'colectivo_validado', 'enviado_en_csv', 'enviado_cupon', ('created', DateRangeFilter), ('updated', DateRangeFilter), ]
    list_display = ['id', 'created', 'updated', 'nombre', 'primer_apellido', 'segundo_apellido', 'email', 'codigo_postal', 'enviado_en_csv', 'enviado_cupon', 'colectivo', 'colectivo_validado', 'acreditacion', 'codigo_cupon', ]
    actions = [
        marcar_enviado_en_csv,
        marcar_cupon_enviado,
        marcar_colectivo_validado,
        marcar_colectivo_no_validado,
        enviar_email_acreditacion_no_valida,
        enviar_email_con_cupon,
    ]
    resource_class = LeadResource


class ColectivoAdmin(admin.ModelAdmin):
    list_display = ['nombre', ]


admin.site.register(Lead, LeadAdmin)
admin.site.register(Colectivo, ColectivoAdmin)
