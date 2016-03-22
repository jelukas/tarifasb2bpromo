# -*- coding: utf-8 -*-
import unicodecsv as csv
import fnmatch
import os
from unipath import Path
from datetime import datetime, timedelta

from django_cron import CronJobBase, Schedule
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Lead
from .utils import recoger_cupones_de_fecha, enviar_csv_ftp


class CsvCreation(CronJobBase):
    RUN_AT_TIMES = ["09:55", "10:55", "11:55", "12:55", "13:55", "14:55", "15:55", "16:55", "17:55", "18:55", "19:55", "20:55"]
    MIN_NUM_FAILURES = 1

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'leads.csv_creation'    # a unique code

    def do(self):
        leads_validos_no_enviados_en_csv = Lead.objects.filter(enviado_en_csv=False, enviado_cupon=False, colectivo_validado=True)
        # with open(settings.CSV_ROOT.child(str(datetime.now().strftime('%d%m%Y%H%M'))+"_test.csv"), 'w+b') as csvfile:
        with open(settings.CSV_ROOT.child("fichero.csv"), 'w+b') as csvfile:
            csv_validos = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            for lead in leads_validos_no_enviados_en_csv:
                csv_validos.writerow([lead.id, lead.nombre, lead.primer_apellido, lead.segundo_apellido])
            csvfile.close()
            leads_validos_no_enviados_en_csv.update(enviado_en_csv=True)
            enviar_csv_ftp(Path(csvfile.name))


class RecogerCuponesDiaAnterior(CronJobBase):
    RUN_AT_TIMES = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
    MIN_NUM_FAILURES = 1

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'leads.recoger_cupones_dia_anterior'    # a unique code

    def do(self):
        hoy = datetime.now()
        dias = timedelta(days=0)
        fecha_dia_anterior = hoy - dias
        recoger_cupones_de_fecha(fecha_dia_anterior)


class CheckAndSendCoupon(CronJobBase):
    RUN_AT_TIMES = ["10:05", "11:05", "12:05", "13:05", "14:05", "15:05", "16:05", "17:05", "18:05", "19:05", "20:05", "21:05"]
    MIN_NUM_FAILURES = 1
    # RUN_EVERY_MINS = 10

    # schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'leads.check_and_send_coupon'

    def do(self):
        leads_validos_y_enviados_en_csv = Lead.objects.filter(enviado_en_csv=True, enviado_cupon=False, colectivo_validado=True)
        for lead in leads_validos_y_enviados_en_csv:
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
                        # mail.attach_file(cupon_fichero.absolute())
                        mail.send()
                        lead.enviado_cupon = True
                        lead.codigo_cupon = codigo
                        lead.save()
