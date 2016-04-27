"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace base.ajax
#
# Contiene las funciones que atienden peticiones ajax de uso general
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
from django.apps import apps

from base.classes import Seniat
from base.functions import verificar_rif
from .constant import MSG_NOT_AJAX, TIPO_PERSONA_LIST

"""!
Contiene el objeto que registra la vitacora de eventos del módulo usuario.
(configuración en el settings de la aplicación)
"""
logger = logging.getLogger("base")

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


def get_data_rif(request):
    if not request.is_ajax():
        return HttpResponse(json.dumps({'result': False, 'message': MSG_NOT_AJAX}))

    rif = request.GET.get('rif', None)
    agente_retencion = request.GET.get('agente_retencion', None)
    contribuyente = request.GET.get('contribuyente', None)
    message = _("No se ha indicado un número de RIF a consultar")

    if rif:
        datos_rif = Seniat()
        seniat = datos_rif.buscar_rif(rif)
        if datos_rif:
            return HttpResponse(json.dumps({'result': True, 'nombre': seniat.nombre}))
        message = _("El RIF no puede ser comprobado")

    return HttpResponse(json.dumps({'result': False, 'message': message}))


def validar_rif_seniat(request):
    if not request.is_ajax():
        return HttpResponse(json.dumps({'result': False, 'message': MSG_NOT_AJAX}))

    rif = request.GET.get('rif', None)
    message = _("No se ha indicado un número de RIF a consultar")

    if rif:
        validar_rif = Seniat()
        if rif[0] not in TIPO_PERSONA_LIST:
            message = _("Tipo de RIF incorrecto")
        elif not rif[1:].isdigit() or not verificar_rif(rif):
            message = _("El RIF es inválido")
        elif not validar_rif.buscar_rif(rif):
            message = _("El RIF no existe")
        else:
            return HttpResponse(json.dumps({'result': True}))

    return HttpResponse(json.dumps({'result': False, 'message': message}))