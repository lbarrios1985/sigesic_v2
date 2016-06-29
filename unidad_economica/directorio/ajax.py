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
                coord = dir.coordenadas.split(",")
                coord = "<span class='pull-left'>Longitud:</span> <span class='pull-right'>%s</span><br/>" \
                        "<span class='pull-left'>Latitud:</span> <span class='pull-right'>%s</span>" % (coord[0], coord[1])

            datos.append([
                dir.parroquia.municipio.estado.nombre, dir.parroquia.municipio.nombre, dir.parroquia.nombre,
                direccion, coord
            ])

            return HttpResponse(json.dumps({'data': datos}))

    except Exception as e:
        message = e

    return HttpResponse(json.dumps({'result': False, 'message': str(message)}))


@login_required()
def add_direccion(request):
    message = _("La dirección no existe")

    try:
        if not request.is_ajax():
            return HttpResponse(json.dumps({'result': False, 'message': MSG_NOT_AJAX}))

        directorio_id = request.GET.get('directorio_id', None)

        if directorio_id:
            direccion = Directorio.objects.get(pk=directorio_id)
            tipo_coordenada = ''
            coordenada = []

            if direccion.tipo_coordenada:
                tipo_coordenada = direccion.tipo_coordenada.pk
                coordenada = direccion.coordenadas.split(",")

            return HttpResponse(json.dumps({
                'resultado': True, 'tipo_vialidad': direccion.tipo_vialidad, 'coordenadas': coordenada,
                'nombre_vialidad': direccion.nombre_vialidad, 'tipo_edificacion': direccion.tipo_edificacion,
                'descripcion_edificacion': direccion.descripcion_edificacion, 'nombre_zona': direccion.nombre_zona,
                'tipo_subedificacion': direccion.tipo_subedificacion, 'tipo_zonificacion': direccion.tipo_zonificacion,
                'descripcion_subedificacion': direccion.descripcion_subedificacion,
                'estado': direccion.parroquia.municipio.estado.pk, 'municipio': direccion.parroquia.municipio.pk,
                'parroquia': direccion.parroquia.pk, 'tipo_coordenada': tipo_coordenada
            }))

    except Exception as e:
        message = e

    return HttpResponse(json.dumps({'result': False, 'error': str(message)}))