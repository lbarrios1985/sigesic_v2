"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace base.fields
#
# Contiene las clases, atributos y métodos para los campos personalizados a implementar en los formularios
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

import logging

from django.forms import MultiValueField, ChoiceField, CharField
from django.utils.translation import ugettext_lazy as _

from .constant import SHORT_TIPO_PERSONA, SHORT_NACIONALIDAD
from .widgets import RifWidget, CedulaWidget

"""!
Contiene el objeto que registra la vitacora de eventos del módulo base.
(configuración en el settings de la aplicación)
"""
logger = logging.getLogger("base")

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


class RifField(MultiValueField):
    """!
    Clase que agrupa los campos del tipo de rif, número de rif y dígito validador del rif en un solo campo del
    formulario

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 26-04-2016
    @version 2.0.0
    """
    widget = RifWidget
    default_error_messages = {
        'invalid_choices': _("Debe seleccionar un tipo de RIF válido")
    }

    def __init__(self, *args, **kwargs):

        error_messages = {
            'required': _("Debe indicar un numero de RIF"),
            'invalid': _("El valor indicado no es válido"),
            'incomplete': _("El número de RIF esta incompleto")
        }

        fields = (
            ChoiceField(choices=SHORT_TIPO_PERSONA),
            CharField(max_length=8, min_length=8),
            CharField(max_length=1, min_length=1)
        )

        label = _("R.I.F.:")

        super(RifField, self).__init__(
            error_messages=error_messages, fields=fields, label=label, require_all_fields=True, *args, **kwargs
        )

    def compress(self, data_list):
        print("data_list = ", data_list)
        if data_list:
            return ''.join(data_list)
        return ''


class CedulaField(MultiValueField):
    """!
    Clase que agrupa los campos de la nacionalidad y número de cédula de identidad en un solo campo del formulario

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 26-04-2016
    @version 2.0.0
    """
    widget = CedulaWidget
    default_error_messages = {
        'invalid_choices': _("Debe seleccionar una nacionalidad válida")
    }

    def __init__(self, *args, **kwargs):

        error_messages = {
            'required': _("Debe indicar un número de Cédula"),
            'invalid': _("El valor indicado no es válido"),
            'incomplete': _("El número de Cédula esta incompleto")
        }

        fields = (
            ChoiceField(choices=SHORT_NACIONALIDAD),
            CharField(max_length=8)
        )

        label = _("Cedula de Identidad:")

        super(CedulaField, self).__init__(
            error_messages=error_messages, fields=fields, label=label, require_all_fields=True, *args, **kwargs
        )

    def compress(self, data_list):
        if data_list:
            return ''.join(data_list)
        return ''