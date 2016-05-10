"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidadeconomica.forms
#
# Formularios para la identificación de la unidad económica
# @author Eveli Ramírez (eramirez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 04-05-2016
# @version 2.0
from __future__ import unicode_literals
from django import forms
from base.fields import RifField, CedulaField

from django.utils.translation import ugettext_lazy as _

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

class unidadEconomicaForm(forms.Form):
    """!
    Formulario para el registro de la unidad económica

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 04-05-2016
    @version 2.0
    """

    ## R.I.F. de la Unidad Económica que identifica al usuario en el sistema
    rif = RifField()

    ## Nombre Comercial de la Unidad Económica
    nombre_ue = forms.CharField(
        label=_("Nombre Comercial: "),
        max_length=30
    )

    ## Razón Social
    razon_social = forms.CharField(
        label=_("Razón Social: "),
        max_length=45,
    )

    ## Número de Plantas Productivas de la Unidad Económica
    nro_planta = forms.IntegerField(
        label=_("Número de Plantas Productivas:"),
    )

    ## Número de Unidades Comercializadoras 
    nro_unid_comercializadora = forms.IntegerField(
        label=_("Número de Unidades Comercializadoras:"),
    )

    ## Servicios que presta la Unidad Económica
    servicio = forms.BooleanField(
        label=_("¿Presta algún servicio?"),
    )

    ## Organización comunal
    orga_comunal = forms.BooleanField(
        label=_("¿Es una organización comunal?"),
    )

    ## Casa Matriz de alguna Franquicia
    casa_matriz_franquicia = forms.BooleanField(
        label=_("¿Es la casa matriz de alguna Franquicia?"),
    )

    ## Número de Franquicias asociadas a la Unidad Económica
    nro_franquicias = forms.IntegerField(
        label=_("Número de Franquicias:"),
    )
