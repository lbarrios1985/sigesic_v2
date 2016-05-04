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

from django.conf import settings
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

## Lista de tipos de persona
TIPO_PERSONA_LIST = [tp[0] for tp in SHORT_TIPO_PERSONA]

## Nacionalidades (ABREVIADO)
SHORT_NACIONALIDAD = (
    ("V", "V"), ("E", "E")
)

## Lista de nacionalidades
NACIONALIDAD_LIST = [nac[0] for nac in SHORT_NACIONALIDAD]

## Turno de atención al público
TURNO = (
    ("M", _("Mañana")),
    ("T", _("Tarde"))
)

## PERIODO DE VERIFICACION DE LA CADUCIDAD DE LA CONTRASEÑA EN DIAS
ACTUALIZACION_PASSWORD = 90

## Nombre del Sitio
APP_NAME = "SIGESIC"

## Asunto del mensaje de bienvenida
EMAIL_SUBJECT_REGISTRO = "Bienvenido a %s" % APP_NAME

admin_email = ''
if settings.ADMINS:
    ## Contiene el correo electrónico del administrador del sistema
    admin_email = settings.ADMINS[0][1]

## Mensaje de bienvenida utilizado en el registro de usuarios
REGISTRO_MESSAGE = '%s %s %s (spam) %s %s' % \
                   (str(_("Hemos enviado un mensaje de bienvenida con un enlace de activación a la dirección de correo "
                          "suministrada.")),
                    str(_("Por favor confirme el registro haciendo click en el enlace enviado por correo (si lo "
                          "prefiere también puede copiar y pegar el enlace en su navegador).")),
                    str(_("En caso de no recibir el correo enviado por el sistema en su bandeja de entrada, "
                          "se le recomienda revisar la carpeta de correos no deseados")),
                    str(_("y verificar si existe, en caso afirmativo le recomendamos agregar la dirección de correo de "
                          "la aplicación en la libreta de direcciones de su cuenta de correo para que en futuras "
                          "ocasiones no sea filtrado. En caso contrario contacte al administrador del sistema")),
                    str(admin_email))

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

## Determina el nivel mínimo de validación para la fortaleza de la contraseña. Los valores permitidos son del 0 al 5
FORTALEZA_CONTRASENHA = 3

## Días de caducidad para el enlace de registro de usuarios
CADUCIDAD_LINK_REGISTRO = 1
