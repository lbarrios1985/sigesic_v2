"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidad_economica.forms
#
# Formularios para la identificación de la unidad económica
# @author Eveli Ramírez (eramirez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 04-05-2016
# @version 2.0
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from base.constant import SELECCION
from base.fields import RifField
from base.widgets import RifWidgetReadOnly

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

class UnidadEconomicaForm(forms.Form):
    """!
    Formulario para el registro de la unidad económica

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 04-05-2016
    @version 2.0
    """

    ## R.I.F. de la Unidad Económica que identifica al usuario en el sistema
    rif = RifField()

    rif.widget = RifWidgetReadOnly()

    ## Nombre Comercial de la Unidad Económica
    nombre_ue = forms.CharField(
        label=_("Nombre Comercial: "),
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Nombre Comercial de la Unidad Económica a registrar"), 'size': '35'
            }
        )
    )

    ## Razón Social
    razon_social = forms.CharField(
        label=_("Razón Social: "),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'readonly': 'readonly',
                'title': _("Razón Social"),
            }
        ), required=False
    )

    ## Número de Plantas Productivas de la Unidad Económica
    nro_planta = forms.IntegerField(
        label=_("Número de Plantas Productivas:"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Número de Plantas Productivas de la Unidad Económica"), 'size': '1'
            }
        )
    )

    ## Número de Unidades Comercializadoras 
    nro_unid_comercializadora = forms.IntegerField(
        label=_("Número de Unidades Comercializadoras:"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Número de Unidades Comercializadoras de la Unidad Económica"), 'size': '1'
            }
        )
    )

    ## Servicios que presta la Unidad Económica
    servicio = forms.ChoiceField(
        label=_("¿Presta algún servicio?"),
        choices=(SELECCION)
    )

    ## Organización comunal
    orga_comunal = forms.ChoiceField(
        label=_("¿Es una organización comunal?"),
        choices=(SELECCION)
    )

    tipo_orga_comunal = forms.CharField(
        label=_("Tipo de Organizacón Comunal: "),
    )

    ## Casa Matriz de alguna Franquicia
    casa_matriz_franquicia = forms.ChoiceField(
        label=_("¿Es la casa matríz de una Franquicia?"),
        choices=(SELECCION)
    )

    ## Número de Franquicias asociadas a la Unidad Económica
    nro_franquicia = forms.IntegerField(
        label=_("Número de Franquicias:"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Número de Franquicias de la Unidad Económica"), 'size': '1'
            }
        )
    )

    ## Franquiciado
    franquiciado = forms.ChoiceField(
        label=_("¿Forma parte de una Franquicia?"),
        choices=(SELECCION)
    )

    ## País de la Franquicia
    pais_franquicia = forms.ChoiceField(
        label=_("País de Origen de la Franquicia"),
        choices=("Seleccione..")
    )
