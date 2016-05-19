"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace sedes_administrativa.constantes
#
# Contiene las constantes a implementar en los modelos y formularios del módulo de sedes_administrativa
# @author Ing. Hugo Ramirez (hramirez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

##TIPOS DE CARRETERAS
TIPO_CARRETERA = (
    ("", _("")),
    ("tierra", _("tierra")),
    ("asfalto", _("asfalto")),
    ("tierra", _("tierra"))
)
##TIPOS DE CARRETERAS
TIPO_EDIFICACION = (
    ("", _("")),
    ("bloque", _("bloque")),
    ("madera", _("madera")),
    ("tierra", _("tierra"))
)
##porcentajes
PORCENTAJE = ([(i, "%s %%" % i) for i in range(0, 100, 1)])
##Ambito industrial de la unidad Economica

## Tenencia
TENENCIA = (
    ("", _("")),
    ("ocupacion", _("Ocupacion")),
    ("arrendada", _("Arrendada")),
    ("comodato", _("Comodatos")),
    ("propia", _("Propia")),
    ("otra", _("Otra"))
)
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
