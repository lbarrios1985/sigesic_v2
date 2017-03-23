"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace carga_masiva.functions
#
# Contiene funciones de uso general para la gestión de datos en carga masiva
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals, absolute_import

import logging
from datetime import datetime
from django.apps import apps

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

logger = logging.getLogger('carga_masiva')
date_now = datetime.now()


def comprobar_datos(app, mod, file, anho=None):
    """!
    Función que permite verificar si los datos del archivo de carga masiva son correctos

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 01-03-2017
    @param app  <b>{string}</b> Nombre de la aplicación que procesará el archivo.
    @param mod  <b>{string}</b> Nombre del modelo que contiene los métodos para procesar los datos.
    @param file <b>{string}</b> Ruta y nombre del archivo a verificar
    @param anho <b>{string}</b> Año para el registro de datos (opcional).
    @return Devuelve Falso si se encontraron errores al comprobar los datos del archivo, de lo contrario retorna
            Verdadero
    """
    instance = apps.get_model(app, mod)
    modelo = instance()

    for m in modelo.cm_fields:
        ## Obtiene el attributo del campo en el modelo
        if 'app' in m and 'mod' in m:
            ## Instancia del modelo relacionado
            rel_instance = apps.get_model(m['app'], m['mod'])
            ## Objeto del modelo instanciado
            rel_modelo = rel_instance()
            campo = rel_modelo._meta.get_field(m['field'])
        else:
            campo = modelo._meta.get_field(m['field'])

        ## Tipo de dato del campo
        data_type = campo.get_internal_type()
        data_null = campo.null
        data_blank = campo.blank


    # Verificar el campo id, si contiene datos realizar la validación, en caso contrario no realizar o incorporar otro método de validación
    return True
