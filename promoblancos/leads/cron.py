
import csv
from datetime import datetime

from django_cron import CronJobBase, Schedule
from django.conf import settings

from .models import Lead


class CsvCreation(CronJobBase):
    RUN_AT_TIMES = ['15:05', '14:00', ]

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'leads.csv_creation'    # a unique code

    def do(self):
        leads_validos_no_enviados_en_csv = Lead.objects.filter(enviado_en_csv=False, enviado_cupon=False, colectivo_validado=True)
        with open(settings.PROJECT_PATH.ancestor(2).child(str(datetime.now().strftime('%d%m%Y%H%M'))+"_test.csv"), 'w+b') as csvfile:
            csv_validos = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            for lead in leads_validos_no_enviados_en_csv:
                csv_validos.writerow([lead.id, lead.nombre, lead.primer_apellido, lead.segundo_apellido])
            csvfile.close()
            leads_validos_no_enviados_en_csv.update(enviado_en_csv=True)
