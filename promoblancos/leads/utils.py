import pysftp
from django.conf import settings


def enviar_csv_ftp(fichero_csv):
    with pysftp.Connection(settings.SFTP_HOST, username=settings.SFTP_USER, password=settings.SFTP_PASS, port=int(settings.SFTP_PORT)) as sftp:
        with sftp.cd('tar_blancas'):
            sftp.put(fichero_csv.absolute())


def recoger_cupones_de_fecha(date_object):
    with pysftp.Connection(settings.SFTP_HOST, username=settings.SFTP_USER, password=settings.SFTP_PASS, port=int(settings.SFTP_PORT)) as sftp:
        sftp.get_d('tar_blancas/'+date_object.strftime('%d%m%Y'), settings.COUPONS_ROOT, preserve_mtime=True)
