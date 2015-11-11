import pysftp
from django.conf import settings


def conectar_enviar_cerrar(fichero):
    with pysftp.Connection(settings.SFTP_HOST, username=settings.SFTP_USER, password=settings.SFTP_PASS, port=int(settings.SFTP_PORT)) as sftp:
        with sftp.cd('tar_blancas'):
            sftp.put(fichero.absolute())
