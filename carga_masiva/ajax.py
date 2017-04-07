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
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import transaction
from django.apps import apps
from django.conf import settings
from datetime import datetime
from base.models import AnhoRegistro

from base.constant import MSG_NOT_AJAX, MSG_NOT_DOWNLOAD_FILE, MSG_NOT_UPLOAD_FILE, EMAIL_SUBJECT_CM_RESULT

import logging
import json
import pyexcel
import csv
import xlwt

from base.functions import enviar_correo

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

        if app and mod and archivo and father_id:
            instance = apps.get_model(app, mod)
            modelo = instance()
            ruta = settings.CARGA_MASIVA_FILES + "/" + str(archivo)
            path = default_storage.save(ruta, ContentFile(archivo.read()))

            ## Evalua si se ha indicado un año de registro
            if anho and anho.rfind('Seleccione') < 0:
                resultado = modelo.carga_masiva_load(path, anho, father_id)
            else:
                resultado = modelo.carga_masiva_load(path=path, rel_id=father_id)

            default_storage.delete(path)

            if (resultado['validacion']):
                return HttpResponse(json.dumps({
                    'result': True, 'message': resultado['message']
                }))

            ## En caso de errores al procesar el archivo se envían los correspondientes mensajes por correo
            msg = str(_(
                'Se han encontrado errores en el archivo a procesar. Verifique los siguientes errores e intente '
                'nuevamente:'
            ))
            if isinstance(resultado['message'], list):
                msg += "<br><ul>"
                for message in resultado['message']:
                    msg += "<li>%s</li>" % message
                msg += "</ul>"
                format_html(msg)
            else:
                msg = resultado['message']

            administrador, admin_email = '', ''
            if settings.ADMINS:
                administrador = settings.ADMINS[0][0]
                admin_email = settings.ADMINS[0][1]

            enviado = enviar_correo(
                request.user.email, 'carga.result.mail', EMAIL_SUBJECT_CM_RESULT % str(app), {
                    'modulo': instance._meta.verbose_name.title(), 'fecha_carga': datetime.now(),
                    'rif': str(request.user.username),
                    'nombre_ue': str(request.user.unidadeconomica_set.values()[0]['nombre_ue']),
                    'error_messages': msg, 'emailapp': settings.EMAIL_FROM, 'administrador': administrador,
                    'admin_email': admin_email
                }
            )

            if not enviado:
                logger.warning(
                    str(_("Ocurrió un inconveniente al enviar el correo de sobre el resultado de registro de datos en "
                          "carga masiva de %s al usuario [%s]") % str(request.username))
                )
                return HttpResponse(json.dumps(
                    {
                        'result': False,
                        'error': str(_("No se pudo enviar el correo de estatus del registro, intente más tarde..."))
                    })
                )

            return HttpResponse(json.dumps({'result': False, 'error': msg}))
        return HttpResponse(json.dumps({'result': False, 'error': str(_('Faltan Párametros'))}))

    except Exception as e:
        message = e

    return HttpResponse(json.dumps({'result': False, 'message': str(message)}))
