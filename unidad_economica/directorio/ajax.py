"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.directorio.ajax
#
# Contiene las funciones que atienden peticiones ajax del directorio
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals, absolute_import

import logging
import json

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required

from base.constant import (
    MSG_NOT_AJAX, PREFIJO_DIRECTORIO_UNO_CHOICES, PREFIJO_DIRECTORIO_DOS_CHOICES, PREFIJO_DIRECTORIO_TRES_CHOICES,
    PREFIJO_DIRECTORIO_CUATRO_CHOICES
)
from .models import Directorio

"""!
Contiene el objeto que registra la vitacora de eventos del módulo usuario.
(configuración en el settings de la aplicación)
"""
logger = logging.getLogger("base")

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


@login_required()
def get_directorio(request):
    """!
    Función que obtiene los datos del directorio

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 27-06-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un HttpResponse con el JSON del listado de direcciones asociadas al usuario
    """

    message = _("No existen direcciones registradas aún")

    try:
        if not request.is_ajax():
            return HttpResponse(json.dumps({'result': False, 'message': MSG_NOT_AJAX}))

        datos = []
        direccion = ''

        for dir in Directorio.objects.filter(usuario=request.user):
            direccion += '<input class="directorio_id" type="hidden" value="%s" readonly="readonly" disabled="disabled" style="display:none">' % dir.pk
            for tv in PREFIJO_DIRECTORIO_UNO_CHOICES:
                if dir.tipo_vialidad in tv[0]:
                    direccion += tv[1] + " "
            direccion += dir.nombre_vialidad + " "
            coord = _("No indicada")
            if dir.coordenadas:
                coord = dir.coordenadas

            datos.append([
                dir.parroquia.municipio.estado.nombre, dir.parroquia.municipio.nombre, dir.parroquia.nombre,
                direccion, coord
            ])

            return HttpResponse(json.dumps({'data': datos}))

    except Exception as e:
        message = e
    print(message)
    return HttpResponse(json.dumps({'result': False, 'message': str(message)}))