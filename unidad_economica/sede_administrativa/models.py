# Create your models here.
"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace sedes_admin.models
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para los  del módulo de usuario
# @author Ing. Hugo Ramirez (hramirez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
#from django.core import validators
from django.db import models

from django.utils.translation import ugettext_lazy as _

from .constantes import TENENCIA, TIPO_CARRETERA, TIPO_EDIFICACION, PORCENTAJE

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

class RegistroSedes(models.Model):
    """clase que conduce el registro de sedes administrativas  """

    ## Establece el nombre de la sede
    nombre_sede = models.CharField(
        max_length=50, help_text=_("Nombre de la sede")
    )
    ## Establece el tipo de carretera de acceso a la sede
    tipo_carretera = models.CharField(
        max_length=50, help_text=_("Tipo de carretera de acceso a la sede")
    )
    ## Establece el nombre de la carretera de acceso
    nombre_carretera = models.CharField(
        max_length=50,choices=TIPO_CARRETERA, help_text=_("Nombre de la carretera de acceso a la sede")
    )
    ## Establece el tipo de edificacion de la sede
    tipo_edificacion = models.CharField(
        max_length=50, choices=TIPO_EDIFICACION , help_text=_("Tipo de edificacion de la sede")
    )
    ## Establece el nombre de la edificacion de la sede
    nombre_edificacion = models.CharField(
        max_length=50, help_text=_("Nombre de la edificacion de la sede")
    )
    ## Establece el nombre del sector donde esta ubicada la sede
    nombre_sector = models.CharField(
        max_length=35, help_text=_("Nombre del sector donde esta ubicada la sede")
    )
    ##Establece la condicion de tenencia de la sedes administrativa
    tipo_tenencia = models.CharField(
        max_length=100, choices=TENENCIA, help_text=_("Tipo de tenencia de la sede administrativa")
    )
    ##Establece los metros cuadrados que posee la sede administrativa
    metros_cuadrados = models.IntegerField(
        help_text=_("Metros cuadrados de la tenencia")
        )
    #Establece los metros cuadrados de construccion que tiene la sede administrativa
    metros_cuadrados_construccion = models.IntegerField(
        help_text=_("Metros cuadrados de construccion de la tenencia")
        )
    ##Establece el porcentaje de autonomia electrica de la sede
    autonomia_electrica = models.IntegerField(
        choices=PORCENTAJE, help_text=_("Porcentaje de autonomia electrica que posee la sede")
     )
     ##Establece el porcentaje de consumo electrico de la sede
    consumo_electrico = models.TextField(
        choices=PORCENTAJE, help_text=_("Porcentaje del consumo electrico en la sede")
     )