"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidad_economica.admin
#
# Clases, atributos y métodos del módulo unidadeconomica a implementar en el panel administrativo 
# @author Eveli Ramírez (eramirez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.contrib import admin

from .models import Notificacion

import logging

logger = logging.getLogger("ue")

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


class NotificacionAdmin(admin.ModelAdmin):
    """!
    Clase que gestiona las notificaciones en el panel administrativo

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2016
    @version 2.0.0
    """
    list_display = ('unidad_economica', 'mensaje', 'estatus')
    list_filter = ('unidad_economica', 'estatus')
    ordering = ('unidad_economica', 'estatus')
    search_fields = ('unidad_economica', 'estatus', 'mensaje')


## Registra el modelo Notificacion en el panel administrativo del sistema
admin.site.register(Notificacion, NotificacionAdmin)