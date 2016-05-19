"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace sedes_admin.forms
#
# Contiene las clases y métodos para los formularios del módulo sedes_admin
# @author Ing. Hugo Ramirez (hramirez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# coding=utf-8
from __future__ import unicode_literals
from unidad_economica.sub_unidad_economica.forms import SubUnidadEconomicaForm
from django.utils.encoding import python_2_unicode_compatible


__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"



@python_2_unicode_compatible
class RegistroSedesForm(SubUnidadEconomicaForm):
    pass
