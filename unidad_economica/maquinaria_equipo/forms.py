"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package maquinaria_equipo
# Formularios para la obtencion de datos de la maquinaria de la sub_unidad_economica
# @author Hugo Ramírez (hramirez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 01-06-2016
# @version 2.0
from __future__ import unicode_literals
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from base.constant import (
    ESTADO_ACTUAL,
)
from base.models import Pais
from base.functions import cargar_pais
#from sub_unidad_economica.models import SubUnidadEconomicaProceso
from .models import mimodelo




__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

class maquinaria(forms.ModelForm):
    proceso =\
        (
            ('#', _("#")),
            ('#', _("#")),
            ('#', _("#")),
        )

    ## nombre del proceso productivo extraido de registro de actividad economica
    nombre_proceso = forms.ChoiceField(
        label=_("Proceso Productivo: "),#queryset=nombre_proceso.objects.all(), empty_label=_("Seleccione..."),
        choices=proceso,
        widget=forms.Select(attrs={
            'class': 'form-control', 'data-toggle': 'tooltip', 'required': 'true',
            'title':_("Selecione el nombre del proceso porductivo al que pertenece la maquinaria o el equipo a registrar"),
            'style': 'width:200px',
        }
        )
    )

    ## Nombre de la maquinaria o el equipo
    nombre_maquinaria = forms.CharField(
        label=_("Nombre Maquinaria: "),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip', 'required': 'true',
                'title':_("Ingrese el nombre que posee la maquinaria o el equipo a registrar"),
                'style': 'width:200px',
            }
        )
    )
    ## País de origen de la maquinaria o el equipo
    pais_origen = forms.ChoiceField(
        label=_("País de Origen: "),
        widget=forms.Select(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip', 'required': 'true',
                'style': 'width:200px',
                'title': _("Seleccione el país de origen de la Maquinario o Equipo")
            }
        )
    )
    ## descripcion de la maquinaria o equipo
    descripcion_maquinaria = forms.CharField(
        label=_("Descripción: "),
        widget=forms.Textarea(
            attrs={
                'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
                'data-toggle': 'tooltip','title': _("Indique la descripción de la Maquinaria o Equipo"),
                'style': 'width:200px',
            })
    )

    ## Estado de la maquinaria o el equipo
    estado_actual = forms.ChoiceField(
        label= _("Estado Actual: "),
        choices= ESTADO_ACTUAL,
        widget=forms.Select(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip', 'required': 'true',
                'title': _("Seleccione el país de origen de la Maquinario o Equipo"),
                'style': 'width:200px',
            }
        )
    )
    ## test years
    AÑO_CHOICES = ('1980', '1981', '1982')

    ## Año de Fabricacion
    """año_fabricacion = ChoiceField(
        label=_("Año de Fabricacion: "),
        choices=AÑO_CHOICES,
        widget=Select(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip', 'required': 'true',
                'title':_("Seleccione el año de fabricacion de la Maquinario o equipo")
            }
        )
    )
    ## Vida Util
    vida_util = IntegerField(
        label=_("Vida Util: "),
        widget=Select(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip', 'required': 'true',
                'title':_("Seleccione el tiempo de vida ultil de la Maquinario o equipo")
            }
        )
    )
    ## Año de Adquisicion
    año_adquisicion = ChoiceField(
        label=_("Año de Fabricacion: "),
        choices=AÑO_CHOICES,
        widget=Select(
            attrs={
                'class': 'form-control','data-toggle': 'tooltip', 'required': 'true',
                'title':_("Seleccione el año de Adquisicion de la Maquinaria o Equipo")
            }
        )
    )"""

    def __init__(self, *args, **kwargs):
        super(maquinaria, self).__init__(*args, **kwargs)

        self.fields['pais_origen'].choices = cargar_pais()

    class Meta:
        model = mimodelo
        fields = '__all__'
