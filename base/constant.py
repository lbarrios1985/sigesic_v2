"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace base.constant
#
# Contiene constantes de uso general en la aplicación
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

## Nacionalidades
NACIONALIDAD = (
    ("V", _("Venezolano")),
    ("E", _("Extranjero"))
)

## TIPOS DE PERSONALIDAD
TIPO_PERSONA = (
    ("V", _("Natural")),
    ("J", _("Jurídica")),
    ("E", _("Extranjera")),
    ("P", _("Pasaporte"))
)

## TIPOS DE PERSONALIDAD (ABREVIADO)
SHORT_TIPO_PERSONA = (
    ("V", "V"), ("J", "J"), ("E", "E"), ("P", "P")
)

## Nacionalidades (ABREVIADO)
SHORT_NACIONALIDAD = (
    ("V", "V"), ("E", "E")
)

## PERIODO DE VERIFICACION DE LA CADUCIDAD DE LA CONTRASEÑA EN DIAS
ACTUALIZACION_PASSWORD = 90

## Mensaje a mostrar al usuario cuando el registro de datos haya sido ejecutado correctamente
CREATE_MESSAGE = _("Los datos fueron registrados correctamente")

## Mensaje a mostrar cuando los datos hayan sido actualizados correctamente
UPDATE_MESSAGE = _("Los datos fueron actualizados correctamente")

## Mensaje a mostrar cuando los datos hayan sido eliminados correctamente
DELETE_MESSAGE = _("El registro seleccionado fue eliminado correctamente")

## Mensaje a mostrar cuando el usuario solicita una nueva contraseña
NUEVA_CLAVE_MESSAGE = _("¡La nueva contraseña fue enviada a su dirección de correo electrónico!")

## Mensaje desautenticación en el sistema
LOGOUT_SECURITY_MESSAGE = _("Por su seguridad usted a sido desautenticado del sistema, debe ingresar nuevamente.")

## Mensaje de error para peticiones AJAX
MSG_NOT_AJAX = _("No se puede procesar la petición. "
                 "Verifique que posea las opciones javascript habilitadas e intente nuevamente.")