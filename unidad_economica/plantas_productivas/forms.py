"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.plantas_productivas.forms
#
# Contiene las clases, atributos y métodos para los formularios a implementar en el módulo de sub unidades economicas
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from django import forms
from django.utils.encoding import python_2_unicode_compatible
from unidad_economica.sub_unidad_economica.forms import SubUnidadEconomicaActividadForm

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

@python_2_unicode_compatible
class PlantasProductivasForm(SubUnidadEconomicaActividadForm):
    """!
    Clase que muestra el formulario de ingreso de plantas productivas (extiende de las actividades de la Sub Unidad)

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 18-05-2016
    @version 2.0.0
    """
    pass