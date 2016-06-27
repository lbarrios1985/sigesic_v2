"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.directorio.admin
#
# Contiene las clases, atributos y métodos básicos del sistema a implementar en el panel administrativo
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.contrib import admin
from .models import TipoCoordenada


import logging

logger = logging.getLogger("ue")

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


class TipoCoordenadaAdmin(admin.ModelAdmin):
    """!
    Clase que gestiona los tipos de coordenadas geográficas

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 27-06-2016
    @version 2.0.0
    """
    list_display = ('tipo',)
    list_filter = ('tipo',)
    ordering = ('tipo',)
    search_fields = ('tipo',)

## Registra el modelo TipoCoordenada en el panel administrativo
admin.site.register(TipoCoordenada, TipoCoordenadaAdmin)