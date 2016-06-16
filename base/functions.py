"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace base.functions
#
# Contiene las funcionas básicas de la aplicación
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

import logging
import smtplib

from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

from .models import CaevClase, TipoComunal, Pais, Estado, Municipio, Parroquia

logger = logging.getLogger('base')

date_now = datetime.now()

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


def verificar_rif(nrorif):
    """!
    Función que permite verificar si el dígito que valida el RIF es el correcto

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 21-04-2016
    @param nrorif <b>{string}</b> Número de R.I.F. a verificar
    @return Devuelve Falso si el número de R.I.F. es incorrecto, en caso contrario devuelve Verdadero
    """

    suma = 0
    divisor = 11
    resto = 0
    digito = 0
    tipo_rif = 0
    digito_validado = 0

    if nrorif.__len__() == 10:

        if nrorif[0:1] == "V" or nrorif[0:1] == "E" or nrorif[0:1] == "J" or nrorif[0:1] == "P" or nrorif[0:1] == "G":
            if nrorif[0:1] == "V":
                tipo_rif = 1
            elif nrorif[0:1] == "E":
                tipo_rif = 2
            elif nrorif[0:1] == "J":
                tipo_rif = 3
            elif nrorif[0:1] == "P":
                tipo_rif = 4
            elif nrorif[0:1] == "G":
                tipo_rif = 5

            suma = ((tipo_rif * 4) + (int(nrorif[1:2]) * 3) + (int(nrorif[2:3]) * 2) + (int(nrorif[3:4]) * 7)
                    + (int(nrorif[4:5]) * 6) + (int(nrorif[5:6]) * 5) + (int(nrorif[6:7]) * 4) + (int(nrorif[7:8]) * 3)
                    + (int(nrorif[8:9]) * 2))

            resto = suma % divisor

            digito_validado = divisor - resto

        if int(digito_validado) >= 10:
            digito_validado = 0

        if int(nrorif[9:10]) == int(digito_validado):
            return True

    return False


def enviar_correo(email, template, subject, vars = None):
    """!
    Función que envía correos electrónicos

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 25-04-2016
    @param email    <b>{string}</b> Dirección de correo electrónico del destinatario.
    @param template <b>{string}</b> Nombre de la plantilla de correo electrónico a utilizar.
    @param subject  <b>{string}</b> Texto del asunto que contendrá el correo electrónico.
    @param vars     <b>{object}</b> Diccionario de variables que serán pasadas a la plantilla de correo. El valor por defecto es Ninguno.
    @return Devuelve verdadero si el correo fue enviado, en caso contrario, devuelve falso
    """
    if not vars:
        vars = {}

    try:
        ## Obtiene la plantilla de correo a implementar
        t = get_template(template)
        c = Context(vars)
        send_mail(subject, t.render(c), settings.EMAIL_FROM, [email], fail_silently=False)
        logger.info("Correo enviado a %s usando la plantilla %s" % (email, template))
        return True
    except smtplib.SMTPException as e:
        logger.error("Ocurrió un error al enviar el correo a [%(correo)s]. Detalles del error: %(error)s" % {
            'correo': email, 'error': e
        }, exc_info=True)
        return False


def calcular_diferencia_fechas(fecha_inicial, fecha_final=date_now):
    """!
    Función que permite calcular la diferencia de días entre dos fechas

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 02-05-2016
    @param fecha_inicial <b>{object}</b> Objeto que contiene el datetime de la fecha inicial
    @param fecha_final <b>{object}</b> Objeto que contiene el datetime de la fecha final. Su valor por defecto,
            si no se especifica, es la fecha actual del sistema
    @return Devuelve la diferencia del número de días entre las dos fechas
    """
    date_format = "%d/%m/%Y"
    fecha_inicial = datetime.strptime(fecha_inicial.strftime(date_format), date_format)
    fecha_final = datetime.strptime(fecha_final.strftime(date_format), date_format)
    diff_dates = fecha_final - fecha_inicial

    return diff_dates.days


def cargar_actividad():
    """!
    Función que permite cargar los datos de las actividades CAEV en una tupla

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 01-06-2016
    @return Devuelve una tupla con las actividades CAEV registradas
    """

    lista = ('', _('Seleccione...')),

    try:
        for act in CaevClase.objects.all():
            lista += (act.clase, act.descripcion),
    except Exception as e:
        pass

    return lista


def cargar_tipo_comunal():
    """!
    Función que permite cargar los datos de los tipos comunales en una tupla

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 01-06-2016
    @return Devuelve una tupla con los tipos comunales
    """

    lista = ('', _('Seleccione...')),

    try:
        for comunal in TipoComunal.objects.all():
            lista += (comunal.id, comunal.tipo_comunal),
    except Exception as e:
        pass

    return lista


def cargar_pais():
    """!
    Función que permite cargar los datos de los países registrados

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 16-06-2016
    @return Devuelve una tupla con los tipos comunales
    """

    lista = ('', _('Seleccione...')),

    try:
        for pais in Pais.objects.all():
            lista += (pais.id, pais.nombre),
    except Exception as e:
        pass

    return lista