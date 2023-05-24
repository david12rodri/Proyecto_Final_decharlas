"""
ASGI config for p_decharlas project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

#Descripcion: Este archivo es el encargado de la configuracion de la aplicacion

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p_decharlas.settings')
application = get_asgi_application()
