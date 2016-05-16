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
from django import forms
from django.forms import (
     ChoiceField, TextInput, CharField, Select, NumberInput
)

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .constantes import (
 TIPO_CARRETERA, TIPO_EDIFICACION, PORCENTAJE, TENENCIA
)
from .models import RegistroSedes

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"



@python_2_unicode_compatible
class RegistroSedesForm(forms.Form):


    ## Nombre de la sede de la unidad economica.
    nombre_sede = CharField(
        label=_("Nombre de la Sede: "),
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'title': _("Nombre de la sede administrativa"),
                'placeholder' : 'Nombre de la sede administrativa',
                'data-rule-required': 'true', 'data-toggle': 'tooltip', 'size': '35',
                're.match': '\s[^0-9]'

            }
        )
    )
    ##Construye el objeto el tipo de carretera
    tipo_carretera = ChoiceField(
        label=_("Tipo de Carretera: "),
        choices=TIPO_CARRETERA,
        widget=Select(
            attrs={
                'class': 'select2 select2-offscreen form-control',
                'title': _("Seleccione el tipo de carretera"),
                'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'style': 'width: 250px;',
                're.match': '[A-Za-z]{10-50}'

            }
        )
    )
    ## Nombre de la carretera de acceso a la sede.
    nombre_carretera = CharField(
        label=_("Nombre Carretera: "),
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'title': _("Nombre de carretera de acceso a la sede administrativa"),
                'placeholder' : 'Nombre de la carretera',
                'data-rule-required': 'true', 'data-toggle': 'tooltip', 'size': '35',
            }
        )
    )
    ##Construye el objeto tipo de edificacion
    tipo_edificacion = ChoiceField(
        label=_("Tipo Edificación: "),
        choices=TIPO_EDIFICACION,
        widget=Select(
            attrs={
                'class': 'select2 select2-offscreen form-control','data-toggle': 'tooltip',
                'title': _("Seleccione el tipo de edificacion de la sede"),
                'data-rule-required': 'true',
                'style': 'width: 250px;',

            }
        )
    )
    ## Nombre de la edificacion
    nombre_edificacion = CharField(
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'title': _("Nombre de la edificacion de la sede administrativa"),
                'placeholder' : 'Nombre de la edificacion',
                'data-rule-required': 'true', 'data-toggle': 'tooltip','size': '35',
            }
        ),
        label=_("Nombre edificación:")
    )
    ## Nombre del sector
    nombre_sector = CharField(
        label=_("Nombre Sector :"),
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'title': _("Nombre del sector donde esta ubicada la sede administrativa"),
                'placeholder': 'Nombre del sector',
                'data-rule-required': 'true', 'data-toggle': 'tooltip','size': '35',
                #'pattern': '',
                're.match': '\w\s'
            }
        )
    )
    ##Define las tenencias
    tipo_tenencia = ChoiceField(
        label=_("Tipo de Tenencia: "),
        choices=TENENCIA,
        widget=Select(
            attrs={
                'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
                'title': _("Seleccione el tipo de tenencia"),
                'data-rule-required': 'true',
                'style': 'width: 250px;',
            }
        )
    )
    ##define los metros cuadrados que possee la sede
    metros_cuadrados = ChoiceField(
        label=_("Metros Cuadrados: "),
        choices=PORCENTAJE,
        widget=NumberInput(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true',
                'title': _("Metros Cuadrados de la sede administrativa"),
                'placeholder' : 'Metros Cuadrados',
                'style': 'width: 250px;',
            }
        )
    )
    ##define los metros cuadrados de la construccion
    metros_cuadrados_construccion = CharField(
        label=_("Metros Cuadrados de Construccio"),
        widget=NumberInput(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true',
                'title': _("Metros Cuadrados de construccion de la sede administrativa"),
                'placeholder' : 'Metros Cuadrados de construccion',
                'style': 'width: 250px;',
            }
        )
    )

    ##define la autonomia electrica
    autonomia_electrica = ChoiceField(
        label=_("Autonomia Electrica: "),
        choices=PORCENTAJE,
        widget=NumberInput(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true',
                'title': _("Autonomia electrica de la sede administrativa"),
                'placeholder' : 'Autonomia electrica',
                'style': 'width: 250px;',
            }
        )
    )
    ##Define el consumo electrico
    consumo_electrico = CharField(
        label=_("Porcentaje de Consumo Electrico: "),
        widget=NumberInput(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
                'data-rule-required': 'true', 'size': '50',
                'title': _("Seleccione el porcentaje de consumo electrico"),
                'placeholder' : 'Consumo electrico',
                'style': 'width: 250px;',


            }
        )
    )
    ##Define el porcentaje de consumo de agua
    consumo_agua = CharField(
        label=_("Porcentaje Consumo de Agua: "),
        widget=NumberInput(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
                'data-rule-required': 'true', 'size': '50',
                'title': _("Seleccione el porcentaje de consumo de agua en la sede"),
                'placeholder' : 'Consumo de Agua',
                'style': 'width: 250px;',


            }
        )
    )
    ##Define el porcentaje de consumo de gas
    consumo_gas = CharField(
        label=_("Porcentaje Consumo de Agua: "),
        widget=NumberInput(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
                'data-rule-required': 'true', 'size': '50',
                'title': _("Seleccione el porcentaje de consumo de gas en la sede"),
                'placeholder' : 'Consumo de gas',
                'style': 'width: 250px;',


            }
        )
    )



class Meta:
    model = RegistroSedes()
    exclude = ['', '', '', '', '', '']

    def clean_nombre_sede(self):
        pass

    def clean_tipo_carretera(self):
        pass

    def clean_nombre_carretera(self):
        pass

# aun faltannnnnn
