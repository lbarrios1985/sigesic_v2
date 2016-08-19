"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace carga_masiva.ajax
#
# Contiene las funciones que atienden peticiones ajax de carga masiva
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals, absolute_import

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.conf import settings

from base.constant import MSG_NOT_AJAX, MSG_NOT_DOWNLOAD_FILE, MSG_NOT_UPLOAD_FILE

import logging
import json
import pyexcel
import csv
import xlwt

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


logger = logging.getLogger("carga_masiva")


@login_required
def descargar_archivo(request):
    """!
    Función que permite construir y descargar un archivo de procesamiento de datos por lostes

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 11-08-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un HttpResponse con el JSON correspondiente al archivo a descargar
    """
    try:
        if not request.is_ajax():
            return HttpResponse(json.dumps({'result': False, 'message': str(MSG_NOT_AJAX)}))

        ## Nombre de la aplicación o módulo
        app = request.GET.get('app', None)

        ## Nombre del modelo en el cual se va a buscar la información a incluir en el archivo
        mod = request.GET.get('mod', None)

        ## Año para el que se esta solicitando el registro de datos
        anho = request.GET.get('anho', None)

        ## Id del modelo relacionado
        rel_id = request.GET.get('rel_id', None)

        if app and mod:
            modelo = apps.get_model(app, mod)
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet("Datos")

            #datos = modelo.objects.carga_masiva_init(anho=None, rel_id=None)
            fields = [
                {
                    'field': 'id',
                    'title': str(_("Registro")),
                    'max_length': 0,
                    'null': False,
                    'type': 'string'
                },
                {
                    'field': 'nombre_maquinaria',
                    'title': str(_("Nombre de la Maquinaria")),
                    'max_length': 100,
                    'null': False,
                    'type': 'string'
                },
                {
                    'field': 'descripcion_maquinaria',
                    'title': str(_("Descripción")),
                    'max_length': 200,
                    'null': False,
                    'type': 'string'
                },
                {
                    'field': 'pais_origen',
                    'title': str(_("País de Fabricación")),
                    'max_length': 100,
                    'null': False,
                    'type': 'string'
                },
                {
                    'field': 'years_fab',
                    'title': str(_("Año de Fabricación")),
                    'max_length': 4,
                    'null': False,
                    'type': 'year'
                },
                {
                    'field': 'date',
                    'title': str(_("Año de Adquisición")),
                    'max_length': 4,
                    'null': True,
                    'type': 'year'
                },
                {
                    'field': 'vida_util',
                    'title': str(_("Vida útil")),
                    'max_length': 2,
                    'null': False,
                    'type': 'integer'
                },
                {
                    'field': 'estado_actual',
                    'title': str(_("Estado Actual")),
                    'max_length': 2,
                    'null': False,
                    'type': 'string'
                }
            ]

            datos = {'cabecera': fields, 'output': 'maquinaria_equipo'}
            font_bold = xlwt.easyxf('font: bold 1')

            i = 0
            for cabecera in datos['cabecera']:
                print(datos['cabecera'][i]['title'])
                sheet.write(0, i, datos['cabecera'][i]['title'], font_bold)
                sheet.col(i).width = 256 * (len(datos['cabecera'][i]['title']) + 1)
                i+=1


            archivo = "%s/%s.xls" % (settings.CARGA_MASIVA_FILES, datos['output'])

            workbook.save(archivo)

            return HttpResponse(json.dumps({
                'resultado': True, 'archivo': archivo, 'message': "El archivo fue generado correctamente"
            }))

        return HttpResponse(json.dumps({'resultado': False, 'error': str(MSG_NOT_DOWNLOAD_FILE)}))
    except Exception as e:
        message = e
    return HttpResponse(json.dumps({'result': False, 'error': str(message)}))

@login_required
def descargar_archivo_apoyo(request):
    """!
    Función que permite construir y descargar un archivo de apoyo con la lista de datos a incluir en la carga masiva

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 11-08-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un HttpResponse con el JSON correspondiente al archivo de apoyo a descargar
    """
    try:
        if not request.is_ajax():
            return HttpResponse(json.dumps({'result': False, 'message': MSG_NOT_AJAX}))

        ## Nombre de la aplicación o módulo
        app = request.GET.get('app', None)

        ## Nombre del modelo en el cual se va a buscar la información a incluir en el archivo
        mod = request.GET.get('mod', None)

        if app and mod:
            pass

        return HttpResponse(json.dumps({'resultado': False, 'error': MSG_NOT_DOWNLOAD_FILE}))
    except Exception as e:
        message = e

    return HttpResponse(json.dumps({'result': False, 'message': str(message)}))


@login_required
def cargar_datos(request):
    try:
        if not request.is_ajax():
            return HttpResponse(json.dumps({'result': False, 'message': MSG_NOT_AJAX}))

        ## Nombre de la aplicación o módulo
        app = request.GET.get('app', None)

        ## Nombre del modelo en el cual se va a buscar la información a incluir en el archivo
        mod = request.GET.get('mod', None)

        ## Año para el que se esta solicitando el registro de datos
        anho = request.GET.get('anho', None)

        if app and mod and anho:
            pass

        return HttpResponse(json.dumps({'resultado': False, 'error': MSG_NOT_UPLOAD_FILE}))
    except Exception as e:
        message = e

    return HttpResponse(json.dumps({'result': False, 'message': str(message)}))
