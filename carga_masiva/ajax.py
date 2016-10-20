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
            datos = instance.carga_masiva_init(anho,rel_id)
            font_bold = xlwt.easyxf('font: bold 1')

            i = 0
            for cabecera in datos['cabecera']:
                sheet.write(0, i, datos['cabecera'][i]['title'], font_bold)
                sheet.col(i).width = 256 * (len(datos['cabecera'][i]['title']) + 1)
                i+=1
                
            #Se obtiene la cantidad de datos
            cantidad = len(datos['datos'])
            #Si existen datos se crean las filas requeridas
            if cantidad > 0:
                for i in range(1,cantidad+1):
                    row = len(datos['cabecera'])
                    for j in range(0,row):
                        sheet.write(i, j, datos['datos'][i-1][j])
                        


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
        
        ## Aplicación de la Relación
        rel_app = request.GET.get('rel_app', None)
        
        ## Modelo de la relación
        rel_mod = request.GET.get('rel_mod', None)
        
        ## Modelo padre
        father_id = request.GET.get('father_id', None)
        
        ## Archivo que se va a cargar
        archivo = request.FILES['file']

        if app and mod and anho and archivo and father_id:
            anho_registro = AnhoRegistro.objects.filter(anho=anho).get()
            instance = apps.get_model(app, mod)
            modelo = instance()
            datos = modelo.carga_masiva_init(anho=anho, rel_id=father_id)
            rel_model = None
            ruta = 'carga_masiva/files/'+str(archivo)
            path = default_storage.save(ruta, ContentFile(archivo.read()))
            load_file = pyexcel.get_sheet(file_name=path)

            for i in range(1,len(load_file.row_range())):
                modelo = instance()
                if(rel_app and rel_mod):
                    instance_rel = apps.get_model(rel_app, rel_mod)
                    rel_model = instance_rel()
                for j in range(len(datos['cabecera'])):
                    if(load_file[0,j]==datos['cabecera'][j]['title']):
                        # Se comprueba si viene algo en la columna id
                        if(datos['cabecera'][j]['title']=='Etiqueta' and load_file[i,j]==''):
                            pass
                        # Se comprueba si el modelo tiene relación
                        elif(datos['cabecera'][j]['related']):
                            # Si tiene una relación con otro modelo
                            if(datos['cabecera'][j]['depend'] and not 'need_object' in datos['cabecera'][j]):
                                model_dep = apps.get_model(datos['cabecera'][j]['related_app'], datos['cabecera'][j]['related_model'])
                                model_dep = model_dep.objects.get(pk=load_file[i,j])
                                setattr(rel_model, datos['cabecera'][j]['field'], model_dep)
                            #Si se requieren modelos externos
                            elif(datos['cabecera'][j]['depend'] and 'need_object' in datos['cabecera'][j]):
                                filtro = {}
                                filtro[datos['cabecera'][j]['filtro']] = load_file[i,j]
                                model_dep = apps.get_model(datos['cabecera'][j]['related_app'], datos['cabecera'][j]['related_model'])
                                model_dep = model_dep.objects.filter(**filtro).get()
                                if(datos['relation']['padre']['mod'] == datos['cabecera'][j]['related_model']):
                                    datos['relation']['padre']['instance'] = model_dep          
                                else:
                                    setattr(rel_model, datos['cabecera'][j]['field'], model_dep)
                                #Si existe una relación doble
                                if('ambigous' in datos['cabecera'][j]):
                                    filtro = {}
                                    filtro[datos['cabecera'][j]['amb_filter']] = getattr(model_dep,datos['cabecera'][j]['amb_field'])
                                    print(filtro)
                                    model_amb = apps.get_model(datos['cabecera'][j]['amb_app'], datos['cabecera'][j]['amb_model'])
                                    model_amb = model_amb.objects.filter(**filtro).get()
                                    setattr(modelo, datos['cabecera'][j]['field'], model_amb)
                            # Si la relación es solo con el padre
                            else:
                                setattr(rel_model, datos['cabecera'][j]['field'], load_file[i,j])
                        else:
                            # Si tiene una relación con otro modelo
                            if(datos['cabecera'][j]['depend'] and not 'need_object' in datos['cabecera'][j]):
                                model_dep = apps.get_model(datos['cabecera'][j]['related_app'], datos['cabecera'][j]['related_model'])
                                model_dep = model_dep.objects.get(pk=load_file[i,j])
                                setattr(modelo, datos['cabecera'][j]['field'], model_dep) 
                            #Si se requieren modelos externos
                            elif(datos['cabecera'][j]['depend'] and 'need_object' in datos['cabecera'][j]):
                                filtro = {}
                                filtro[datos['cabecera'][j]['filtro']] = load_file[i,j]
                                model_dep = apps.get_model(datos['cabecera'][j]['related_app'], datos['cabecera'][j]['related_model'])
                                model_dep = model_dep.objects.filter(**filtro).get()
                                if(datos['relation']['padre']['mod'] == datos['cabecera'][j]['related_model']):
                                    datos['relation']['padre']['instance'] = model_dep
                                else:
                                    setattr(modelo, datos['cabecera'][j]['field'], model_dep)
                                 #Si existe una relación doble
                                if('ambigous' in datos['cabecera'][j]):
                                    filtro = {}
                                    filtro[datos['cabecera'][j]['filtro']] = load_file[i,j]
                                    model_amb = apps.get_model(datos['cabecera'][j]['amb_app'], datos['cabecera'][j]['amb_model'])
                                    model_amb = model_amb.objects.filter(**filtro).get()
                                    setattr(rel_model, datos['cabecera'][j]['field'], model_amb)
                            # Si no tiene relación de ningun otro tipo
                            else:
                                setattr(modelo, datos['cabecera'][j]['field'], load_file[i,j])
                # Se comprueba quien es el hijo del padre (si el modelo o el relacionado)
                if(datos['relation']['padre']['child']==mod):
                    setattr(modelo, datos['relation']['padre']['field'], datos['relation']['padre']['instance'])
                elif(rel_model):
                    setattr(rel_model, datos['relation']['padre']['field'], datos['relation']['padre']['instance'])
                    rel_model.save()
                #Se guarda el año de registro
                setattr(modelo, 'anho_registro', anho_registro)
                #Si existe un relación con un padre, se guarda luego de que se almacene el modelo
                if(rel_model):
                    setattr(modelo, datos['relation']['relation_model']['field'], rel_model)
                modelo.save()
            default_storage.delete(path)
            return HttpResponse(json.dumps({
                'result': True, 'message': "El archivo se cargó éxitosamente'"
            }))

        return HttpResponse(json.dumps({'result': False, 'error': MSG_NOT_UPLOAD_FILE}))
    except Exception as e:
        message = e

    return HttpResponse(json.dumps({'result': False, 'message': str(message)}))
