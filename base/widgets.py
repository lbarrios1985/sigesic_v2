"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace base.widgets
#
# Contiene las clases, atributos y métodos para los widgets a implementar en los formularios
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

import logging

from django.forms import MultiWidget, Select, TextInput
from django.utils.translation import ugettext_lazy as _

from .constant import SHORT_TIPO_PERSONA, SHORT_NACIONALIDAD

"""!
Contiene el objeto que registra la vitacora de eventos del módulo base.
(configuración en el settings de la aplicación)
"""
logger = logging.getLogger("base")

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


class RifWidget(MultiWidget):
    """!
    Clase que agrupa los widgets de los campos del tipo de rif, número de rif y dígito validador del rif

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 26-04-2016
    @version 2.0.0
    """

    def __init__(self, *args, **kwargs):

        widgets = (
            Select(
                attrs={
                    'class': 'select2 form-control', 'data-toggle': 'tooltip',
                    'title': _("Seleccione el tipo de R.I.F.")
                }, choices=SHORT_TIPO_PERSONA
            ),
            TextInput(
                attrs={
                    'class': 'form-control input-sm text-center', 'placeholder': _("Nro. de R.I.F."),
                    'data-toggle': 'tooltip', 'maxlength': '8', 'size':'7', 'data-rule-required': 'true',
                    'title': _("Indique el número de R.I.F., si es menor a 8 dígitos complete con ceros a la izquierda")
                }
            ),
            TextInput(
                attrs={
                    'class': 'form-control input-sm text-center', 'data-rule-required': 'true',
                    'title': _("Indique el último dígito del R.I.F."), 'placeholder': 'X', 'maxlength': '1',
                    'size': '1', 'data-toggle': 'tooltip',
                }
            )
        )

        super(RifWidget, self).__init__(widgets, *args, **kwargs)

    def format_output(self, rendered_widgets):
        return ' - '.join(rendered_widgets)

    def decompress(self, value):
        print("value = ", value)
        if value:
            return [value[0], value[1], value[2]]
        return [None, None, None]


class CedulaWidget(MultiWidget):
    """!
    Clase que agrupa los widgets de los campos de nacionalidad y número de cédula de identidad

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 26-04-2016
    @version 2.0.0
    """

    def __init__(self, *args, **kwargs):

        widgets = (
            Select(
                attrs={
                    'class': 'select2 form-control', 'data-toggle': 'tooltip',
                    'title': _("Seleccione la nacionalidad")
                }, choices=SHORT_NACIONALIDAD
            ),
            TextInput(
                attrs={
                    'class': 'form-control input-sm text-center', 'placeholder': _("Nro. de Cédula"),
                    'data-toggle': 'tooltip', 'maxlength': '8', 'size':'7', 'data-rule-required': 'true',
                    'title': _("Indique el número de Cédula de Identidad")
                }
            )
        )

        super(CedulaWidget, self).__init__(widgets, *args, **kwargs)

    def format_output(self, rendered_widgets):
        return ' - '.join(rendered_widgets)

    def decompress(self, value):
        if value:
            return [value[0], value[1]]
        return [None, None]