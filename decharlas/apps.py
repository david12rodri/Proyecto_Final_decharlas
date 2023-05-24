#Descripcion: Archivo de configuracion de la app decharlas

from django.apps import AppConfig


class DecharlasConfig(AppConfig):  # pylint: disable=too-few-public-methods
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'decharlas'
