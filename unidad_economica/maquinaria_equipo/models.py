"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace maquinaria_equipos .models
#
# Models del módulo maquinaria_equipos
# @author Hugo Ramirez (hramirez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 09-06-2016
# @version 2.0

from django.db import models
from django.utils.translation import ugettext_lazy as _
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomicaProceso
# Create your models here.

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

class maquinariaModel(models.Model):

    """!
    @author Hugo Ramirez (hramirez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-06-2016
    @version 2.0.0
    """

    proceso_sub_unidad = models.ForeignKey(SubUnidadEconomicaProceso)

    nombre_maquinaria = models.CharField(max_length=100)

    pais_origen = models.CharField(max_length=100)

    descripcion_maquinaria = models.CharField(max_length=200)

    years_fab = models.DateField()

    date = models.DateField(blank=False)

    vida_util = models.IntegerField()

    estado_actual = models.CharField(max_length=2)

    def __str__(self):
        return self.nombre_sub


