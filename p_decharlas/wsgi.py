"""
WSGI config for p_decharlas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

#Descripcion: Archivo de configuracion de WSGI para el proyecto.

from django.core.wsgi import get_wsgi_application
import os

# Se establece la configuracion de DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p_decharlas.settings')
# Se obtiene la aplicacion WSGI
application = get_wsgi_application()
