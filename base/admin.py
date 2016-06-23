"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace base.admin
#
# Contiene las clases, atributos y métodos básicos del sistema a implementar en el panel administrativo
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.contrib import admin

from .models import AnhoRegistro

import logging

logger = logging.getLogger("base")

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


class AnhoRegistroAdmin(admin.ModelAdmin):
    """!
    Clase que gestiona los años de registro en el panel administrativo

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2016
    @version 2.0.0
    """
    list_display = ('anho',)
    list_filter = ('anho',)
    ordering = ('anho',)
    search_fields = ('anho',)


## Registra el modelo AnhoRegistro en el panel administrativo
admin.site.register(AnhoRegistro, AnhoRegistroAdmin)