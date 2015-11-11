
import csv
import fnmatch
import os
from unipath import Path
from datetime import datetime, timedelta

from django_cron import CronJobBase, Schedule
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .models import Lead
from .utils import recoger_cupones_de_fecha


class CsvCreation(CronJobBase):
    RUN_AT_TIMES = ['21:30']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'leads.csv_creation'    # a unique code

    def do(self):
        leads_validos_no_enviados_en_csv = Lead.objects.filter(enviado_en_csv=False, enviado_cupon=False, colectivo_validado=True)
        # with open(settings.CSV_ROOT.child(str(datetime.now().strftime('%d%m%Y%H%M'))+"_test.csv"), 'w+b') as csvfile:
        with open(settings.CSV_ROOT.child(str(datetime.now().strftime('%Y%m%d'))+"_test.csv"), 'w+b') as csvfile:
            csv_validos = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            for lead in leads_validos_no_enviados_en_csv:
                csv_validos.writerow([lead.id, lead.nombre, lead.primer_apellido, lead.segundo_apellido])
            csvfile.close()
            leads_validos_no_enviados_en_csv.update(enviado_en_csv=True)


class RecogerCuponesDiaAnterior(CronJobBase):
    RUN_AT_TIMES = ['22:48']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'leads.recoger_cupones_dia_anterior'    # a unique code

    def do(self):
        hoy = datetime.now()
        dias = timedelta(days=1)
        fecha_dia_anterior = hoy - dias
        recoger_cupones_de_fecha(fecha_dia_anterior)


class CheckAndSendCoupon(CronJobBase):
    RUN_AT_TIMES = ['22:45']
    # RUN_EVERY_MINS = 10

    # schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'leads.check_and_send_coupon'

    def do(self):
        leads_validos_y_enviados_en_csv = Lead.objects.filter(enviado_en_csv=True, enviado_cupon=False, colectivo_validado=True)
        for lead in leads_validos_y_enviados_en_csv:
            for fichero in os.listdir(settings.COUPONS_ROOT):
                if fnmatch.fnmatch(fichero, str(lead.id)+'-*.pdf'):
                    cupon_fichero = Path(settings.COUPONS_ROOT, fichero)
                    if cupon_fichero.exists():
                        codigo = fichero.split("-")[1].split(".")[0]
                        mail = EmailMultiAlternatives(
                            subject="Aqui tienes tu cupon",
                            body="Este es el cupon "+codigo+".",
                            from_email="Jesus via JueguetesBlancos <jesus@jesuslucas.com>",
                            to=['jelukas89@gmail.com']
                        )
                        # mail.attach_alternative("<p>Este es tu cuponcinto <strong>"+codigo+" </strong></p>", "text/html")
                        # mail.attach_file(cupon_fichero.absolute())
                        mail.send()
                        lead.enviado_cupon = True
                        lead.codigo_cupon = codigo
                        lead.save()
