"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace carga_masiva.procesar_info
#
# Contiene las clases, atributos, métodos y/o validaciones de carga masiva
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from settings import ADMINS

import pyexcel
import logging

logger = logging.getLogger("carga_masiva")

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


class ProcesarDatos():
	"""!
    Clase que gestiona los datos a cargar en el sistema mediante la opción de carga masiva

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 03-08-2016
    @version 2.0.0
    """

    # EXPRESIONES REGULARES PARA LAS VALIDACIONES
    STRING_100 = ["^(.{1,100})$", _("El campo no debe estar vacío ni ser mayor a 100 caracteres")]
    DECIMAL =  ["^(\d+|\d+\.\d{1,2})$", _("El campo debe ser un número mayor a cero con un máximo de 2 decimales: Ejem: 4,98 ; 0,01 ")]
    DECIMAL_4 =  ["^(\d+|\d+\.\d{1,4})$", _("El campo debe ser un número mayor a cero con un máximo de 4 decimales: Ejem: 4,9855 ; 0,01 ")]
    DECIMAL_IGUAL_0 = ["^(\d+|\d+\.\d{1,2})$", _("El campo debe ser un número igual o mayor que cero con un máximo de 2 decimales: Ejem: 4,98 ; 0 ")]
    ENTERO = ["^(\d{1,12})$", _("El campo debe ser un número entero mayor a cero y no puede contener más de 12 dígitos")]
    ENTERO_MAYOR_0 = ["^([1-9]\d{0,11})$", _("El campo debe ser un número entero mayor a 0 y no puede contener más de 12 dígitos")]
    ENTERO_MAYOR_0_MENOR_50 = ["^([1-9]\d{0,11})$", _("El campo debe ser un número entero mayor a 0 y menor o igual a 50, además no puede contener más de 12 dígitos")]
    ENTERO_MAYOR_IGUAL_0 = ["^([0-9]\d{0,11})$", _("El campo debe ser un número entero mayor o igual a 0 y no puede contener más de 12 dígitos")]
    TEXT = ["^(.(?s){1,10000})$", _("El campo no debe estar vacío ni ser mayor a 10000 caracteres")]
    COD_ARANCELARIO = ["^(\d{4})\.(\d{2})\.(\d{2})\.(\d{2})$", _("El Código arancelario \"%s\" no es válido. Ejemplo de Formato: 8507.10.00.00 . El tamaño máximo de caracteres es de 13")]
    COD_CIIU = ["^(\d{4})$", _("Este valor debe ser un número entero de 4 dígitos, ejemplo: 0111")]
    V_E = ["^(V|E)$", _("Los valores válidos son: V ó E, tamaño del campo = 1")]
    RIF = ["^(V|E|P|J|G{1})(\d{8})(\d{1})$", _("El valor esperado es un RIF y debe tener un formato como este: J123456781, tamaño máximo del campo = 10")]
    RIF_O_NO = ["(^$|^(\s+)$|^(V|E|P|J|G{1})(\d{8})(\d{1})$)", _("RIF no válido, ejemplo: J123456781, tamaño del campo = 10")]
    PAIS = ["^([A-Z]{1}.{1,100})$", _("El campo no debe estar vacío ni ser mayor a 100 caracteres")]
    SI_NO = ["^(SI|NO)$", _("Los valores permitidos son: SI o NO")]
    
    
    CORREOADMIN = str.join(',',[correo for usuario,correo in ADMINS])
    CORREO_UE = None

    def __init__(self, archivo):

        ## Obtiene los registros en el archivo de carga masiva proporcionado por el usuario en un arreglo, en caso de un archivo csv la longitud de cada arreglo es de 1 elemento
        datos = pyexcel.get_sheet(file_name=archivo)

        for dat in datos:
            if dat.__len__() == 0:
                # Es un archivo csv
            else:
                # Esta en otro formato ods, xls, xlsx, etc

    	pass

	#def validar_string()