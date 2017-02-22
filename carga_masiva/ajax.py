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
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import transaction
from django.apps import apps
from django.conf import settings
from base.models import AnhoRegistro

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

        ## Id correspondiente al padre
        rel_id = request.GET.get('rel_id', None)

        if app and mod:
            modelo = apps.get_model(app, mod)
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet("Datos")
            instance = modelo()
            datos = instance.carga_masiva_init(anho, rel_id)
            font_bold = xlwt.easyxf('font: bold 1')

            i = 0
            for cabecera in datos['cabecera']:
                sheet.write(0, i, datos['cabecera'][i]['title'], font_bold)
                sheet.col(i).width = 256 * (len(datos['cabecera'][i]['title']) + 1)
                i += 1

            # Se obtiene la cantidad de datos
            cantidad = len(datos['datos'])
            # Si existen datos se crean las filas requeridas
            if cantidad > 0:
                for i in range(1, cantidad + 1):
                    row = len(datos['cabecera'])
                    for j in range(0, row):
                        sheet.write(i, j, datos['datos'][i - 1][j])

            nombre = rel_id + "_" + datos['output']

            archivo = "%s/%s.xls" % (settings.CARGA_MASIVA_FILES, nombre)

            workbook.save(archivo)

            return HttpResponse(json.dumps({
                'resultado': True, 'archivo': nombre, 'message': "El archivo fue generado correctamente"
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
def retornar_archivo(request):
    """!
    Función que retorna un archivo en la respuesta (si existe)

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 12-12-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un HttpResponse con el JSON correspondiente al archivo de apoyo a descargar
    """
    try:
        # if not request.is_ajax():
        #    return HttpResponse(json.dumps({'result': False, 'message': str(MSG_NOT_AJAX)}))

        filename = request.GET.get('nombre', None)
        if (filename):
            open_file = settings.CARGA_MASIVA_FILES + filename
            # response = HttpResponse()
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            response['X-Sendfile'] = open_file
            return response
        return HttpResponse(False)

    except Exception as e:
        message = e

    return HttpResponse(json.dumps({'result': False, 'message': str(message)}))


@login_required
@transaction.atomic
def cargar_datos(request):
    """!
    Función para cargar los datos de carga masiva

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)/ Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 11-08-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un HttpResponse con el JSON correspondiente al estado de la petición
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

        ## Modelo padre
        father_id = request.GET.get('father_id', None)

        ## Archivo que se va a cargar
        archivo = request.FILES['file']

        if app and mod and anho and archivo and father_id:
            instance = apps.get_model(app, mod)
            modelo = instance()
            datos = modelo.carga_masiva_init(anho=anho, rel_id=father_id)
            ruta = settings.CARGA_MASIVA_FILES + str(archivo)
            path = default_storage.save(ruta, ContentFile(archivo.read()))
            resultado = modelo.carga_masiva_load(path, anho, father_id)

            default_storage.delete(path)

            if (resultado['validacion']):
                return HttpResponse(json.dumps({
                    'result': True, 'message': resultado['message']
                }))
            return HttpResponse(json.dumps({'result': False, 'error': resultado['message']}))
        return HttpResponse(json.dumps({'result': False, 'error': str(_('Faltan Párametros'))}))

    except Exception as e:
        message = e

    return HttpResponse(json.dumps({'result': False, 'message': str(message)}))
