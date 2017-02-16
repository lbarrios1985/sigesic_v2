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
from .models import AnhoRegistro
from .constant import MSG_NOT_AJAX, TIPO_PERSONA_LIST
from sigesic.settings import STATICFILES_DIRS
from unidad_economica.models import CertificadoRegistro, UnidadEconomica

"""!
Contiene el objeto que registra la vitacora de eventos del módulo usuario.
(configuración en el settings de la aplicación)
"""
logger = logging.getLogger("base")

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


def get_data_rif(request):
    """!
    Función que obtiene los datos de un RIF consultado

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 27-04-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un HttpResponse con el JSON correspondiente a los resultados de la consulta
    """
    try:
        if not request.is_ajax():
            return HttpResponse(json.dumps({'result': False, 'message': str(MSG_NOT_AJAX)}))

        rif = request.GET.get('rif', None)
        agente_retencion = request.GET.get('agente_retencion', None)
        contribuyente = request.GET.get('contribuyente', None)
        message = _("No se ha indicado un número de RIF a consultar")

        if rif:
            datos_rif = Seniat()
            seniat = datos_rif.buscar_rif(rif)

            if seniat:
                if datos_rif.error:
                    return HttpResponse(json.dumps({
                        'result': True, 'nombre': datos_rif.nombre, 'error_message': str(datos_rif.error)
                    }))
                return HttpResponse(json.dumps({'result': True, 'nombre': datos_rif.nombre}))

            message = _("El RIF no puede ser comprobado")
    except Exception as e:
        message = e

    return HttpResponse(json.dumps({'result': False, 'message': str(message)}))


def validar_rif_seniat(request):
    """!
    Función que valida si un número de RIF se encuentra bien estructurado

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 27-04-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un HttpResponse con el JSON correspondiente a los resultados de la consulta
    """
    message = _("No se ha indicado un número de RIF a consultar")
    try:
        if not request.is_ajax():
            return HttpResponse(json.dumps({'result': False, 'message': str(MSG_NOT_AJAX)}))

        rif = request.GET.get('rif', None)

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
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps({'result': False, 'message': str(message)}))


@login_required()
def cargar_combo(request):
    """!
    Función que carga datos de un modelo en un select

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 28-04-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un HttpResponse con el JSON correspondiente a los resultados de la consulta y los respectivos
            elementos a cargar en el select
    """
    try:
        if not request.is_ajax():
            return HttpResponse(json.dumps({'resultado': False, 'error': str(MSG_NOT_AJAX)}))

        ## Nombre de la aplicación o módulo
        app = request.GET.get('app', None)

        ## Nombre del modelo en el cual se va a buscar la información a mostrar
        mod = request.GET.get('mod', None)

        ## Atributo del cual se va a obtener el valor a registrar en las opciones del combo resultante
        n_value = request.GET.get('n_value', None)

        ## Atributo del cual se va a obtener el texto a registrar en las opciones del combo resultante
        n_text = request.GET.get('n_text', None)

        ## Nombre de la base de datos en donde buscar la información, si no se obtiene el valor por defecto es default
        bd = request.GET.get('bd', 'default')

        if app and mod and n_value and n_text:
            modelo = apps.get_model(app, mod)
            out = "<option value=''>%s...</option>" % str(_("Seleccione"))
            for o in modelo.objects.using(bd).all():
                out = "%s<option value='%s'>%s</option>" \
                      % (out, str(o.__getattribute__(n_value)),o.__getattribute__(n_text).encode("utf-8"))

            return HttpResponse(json.dumps({'resultado': True, 'combo_html': out}))

        return HttpResponse(json.dumps({'resultado': False, 'error': str(_('No hay registros que actualizar'))}))

    except Exception as e:
        return HttpResponse(json.dumps({'resultado': False, 'error': e}))


@login_required()
def actualizar_combo(request):
    """!
    Función que actualiza los datos de un select dependiente de los datos de otro select

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 28-04-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un HttpResponse con el JSON correspondiente a los resultados de la consulta y los respectivos
            elementos a cargar en el select
    """
    try:
        if not request.is_ajax():
            return HttpResponse(json.dumps({'resultado': False, 'error': str(MSG_NOT_AJAX)}))

        ## Valor del campo que ejecuta la acción
        cod = request.GET.get('opcion', None)

        ## Nombre de la aplicación del modelo en donde buscar los datos
        app = request.GET.get('app', None)

        ## Nombre del modelo en el cual se va a buscar la información a mostrar
        mod = request.GET.get('mod', None)
        
        ## Atributo por el cual se va a filtrar la información
        campo = request.GET.get('campo', None)

        ## Atributo del cual se va a obtener el valor a registrar en las opciones del combo resultante
        n_value = request.GET.get('n_value', None)

        ## Atributo del cual se va a obtener el texto a registrar en las opciones del combo resultante
        n_text = request.GET.get('n_text', None)

        ## Nombre de la base de datos en donde buscar la información, si no se obtiene el valor por defecto es default
        bd = request.GET.get('bd', 'default')

        filtro = {}

        if app and mod and campo and n_value and n_text and bd:
            modelo = apps.get_model(app, mod)
            
            if cod:
                filtro = {campo: cod}

            out = "<option value=''>%s...</option>" % str(_("Seleccione"))

            combo_disabled = "false"

            if cod != "" and cod != "0":
                for o in modelo.objects.using(bd).filter(**filtro).order_by(n_text):
                    out = "%s<option value='%s'>%s</option>" \
                          % (out, str(o.__getattribute__(n_value)),
                             o.__getattribute__(n_text))
            else:
                combo_disabled = "true"

            return HttpResponse(json.dumps({'resultado': True, 'combo_disabled': combo_disabled, 'combo_html': out}))

        else:
            return HttpResponse(json.dumps({'resultado': False,
                                            'error': str(_('No se ha especificado el registro'))}))

    except Exception as e:
        return HttpResponse(json.dumps({'resultado': False, 'error': e}))


@login_required()
def eliminar_registro(request):
    """!
    Función que permite eliminar registros del sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 28-04-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un HttpResponse con el JSON correspondiente a los resultados de la eliminación de datos
    """
    if not request.is_ajax():
        return HttpResponse(json.dumps({'resultado': False, 'msg': str(MSG_NOT_AJAX)}))

    app_label = request.GET.get('app_label', None)
    modelo = request.GET.get('modelo', None)
    id = request.GET.get('id', None)

    if app_label and modelo and id:
        try:
            tabla = apps.get_model(app_label, modelo)
            registro = tabla.objects.get(pk=id)
            registro.delete()
        except Exception as e:
            return HttpResponse(json.dumps({'resultado': False, 'error': e}))

        return HttpResponse(json.dumps({'resultado': True}))

    return HttpResponse(json.dumps({'resultado': False, 'error': str(_("Registro no se puede eliminar"))}))


@login_required()
def anho_registro(request):
    """!
    Función que determina el año de registro para la Unidad Económica Actualmente autenticada en el sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 01-08-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un HttpResponse con el JSON correspondiente a los años para el registro de datos de producción
    """
    if not request.is_ajax():
        return HttpResponse(json.dumps({'resultado': False, 'msg': str(MSG_NOT_AJAX)}))

    anhos = []
    try:
        ue = UnidadEconomica.objects.get(rif=request.user)

        for ae in AnhoRegistro.objects.all().exclude(anho__in=[cert.anho_registro for cert in CertificadoRegistro.objects.filter(ue=ue)]):
            anhos.append(ae.anho)
    except Exception as e:
        print(e)

    if anhos:
        return HttpResponse(json.dumps({'resultado': True, 'anhos': anhos}))

    return HttpResponse(json.dumps({'resultado': False, 'error': str(_("Ya ha registrado todos los años requeridos"))}))

@login_required()
def client_data(request):
    """!
    Función que permite cargar un párametro de un modelo en una aplicación pasados por GET

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-07-2016
    @param request <b>{object}</b> Objeto que contiene la petición a la función
    @return Devuelve un json con el resultado de la búsqueda
    """
    
    app = request.GET['aplicacion']
    model = request.GET['model']
    argument = request.GET['argument']
    field = request.GET['field']
    value = request.GET['value']
    modelo = apps.get_model(app, model)
    a = {}
    a[field] = argument
    search = modelo.objects.filter(**a).values_list(value,flat=True)
    if(len(search)>0):
        return HttpResponse(json.dumps({'resultado': True, 'model': json.dumps(search[0])}))
    return HttpResponse(json.dumps({'resultado': False, 'model': "No se encontraron resultados"}))


@login_required()
def count_model(request):
    """!
    Función que permite mostrar la cantidad de registros de un modelo en una aplicación pasados por GET

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-10-2016
    @param request <b>{object}</b> Objeto que contiene la petición a la función
    @return Devuelve un json con el resultado de la búsqueda
    """
    
    app = request.GET['aplicacion']
    model = request.GET['model']
    argument = request.GET['argument']
    field = request.GET['field']
    modelo = apps.get_model(app, model)
    a = {}
    a[field] = argument
    search = len(modelo.objects.filter(**a).all())
    
    return HttpResponse(json.dumps({'resultado': True, 'cantidad': search}))


def datatable_json(request):
    """!
    Función para montar el json en español de los datatable

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 16-02-2018
    @param request <b>{object}</b> Objeto que contiene la petición a la función
    @return Devuelve un json con el resultado de la búsqueda
    """
    datos = open(STATICFILES_DIRS[0]+"tools/datatables/language/Spanish.json",'r').read()
    datos = json.loads(datos)
    return HttpResponse(json.dumps(datos))