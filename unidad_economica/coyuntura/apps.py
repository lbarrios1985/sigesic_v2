"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidad_economica.coyuntura.apps
#
# Clases, atributos y métodos para la configuración del módulo coyuntura
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>

from django.apps import AppConfig

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

class CoyunturaConfig(AppConfig):
    name = 'coyuntura'
