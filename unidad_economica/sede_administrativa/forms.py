"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace sedes_administrativa.forms
#
# Contiene las clases y métodos para los formularios del módulo sedes_administrativa
# @author Ing. Hugo Ramirez (hramirez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# coding=utf-8
from __future__ import unicode_literals
from django import forms
from base.fields import RifField
from base.models import *
from base.widgets import RifWidgetReadOnly
from unidad_economica.sub_unidad_economica.forms import SubUnidadEconomicaForm
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"



@python_2_unicode_compatible
class RegistroSedesForm(SubUnidadEconomicaForm):

    """## R.I.F. de la Unidad Económica que identifica al usuario en el sistema
    rif = RifField()
    rif.widget = RifWidgetReadOnly()

    ## Nombre Comercial de la Unidad Económica
    nombre_ue = forms.CharField(
        label=_("Nombre Comercial: "),
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Nombre Comercial de la Unidad Económica a registrar"), 'size': '50'
            }
        )
    )

    ## Razón Social
    razon_social = forms.CharField(
        label=_("Razón Social: "),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'readonly': 'readonly',
                'title': _("Razón Social"), 'size': '50',
            }
        ), required=False
    )"""
    pass
