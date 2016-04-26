"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace base.forms
#
# Contiene las clases, atributos y métodos para los formularios a implementar en el módulo de usuario
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

import logging

from django.forms import MultiWidget, Select, TextInput, MultiValueField, ChoiceField, CharField
from django.utils.translation import ugettext_lazy as _

from .constant import SHORT_TIPO_PERSONA

"""!
Contiene el objeto que registra la vitacora de eventos del módulo base.
(configuración en el settings de la aplicación)
"""
logger = logging.getLogger("base")

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

