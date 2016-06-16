"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package maquinaria_equipos.forms
#
# Forms del módulo maquinaria_equipos
# @author Hugo Ramírez (hramirez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 09-06-2016
# @version 2.0
from __future__ import unicode_literals
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from base.models import Pais
from .models import maquinariaModel
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica, SubUnidadEconomicaProceso, SubUnidadEconomicaPrincipalProceso

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

class maquinariaForm(forms.ModelForm):
    proceso =\
        (
            ('#', _("#")),
            ('#', _("#")),
            ('#', _("#")),
        )
    #consulta = Model.objects.all().values('campo_relacion__nombre_campo')

    ## nombre del proceso productivo extraido de registro de actividad economica
    sub_unidad_economica = forms.ModelChoiceField(
        label=_("Sub Unidad Economica: "), queryset=SubUnidadEconomica.objects.all().order_by('id'), empty_label=_("Seleccione..."),
        widget=forms.Select(attrs={
            'placeholder':'Ingrese nombre de Sub unidad economica',
            'class': 'form-control', 'data-toggle': 'tooltip', 'required': 'true',
            'title':_("Selecione el nombre de a sub unidad economica al que pertenece la maquinaria o el equipo a registrar"),
            'style': 'width:200px',
            'onchange': "actualizar_combo(this.value,'unidad_economica.sub_unidad_economica','SubUnidadEconomicaPrincipalProceso','sub_unidad_economica','sub_unidad_economica_proceso__pk','sub_unidad_economica_proceso__nombre_proceso','id_nombre_proceso')"
        }
        )
    )

     ## nombre del proceso productivo extraido de registro de actividad economica
    nombre_proceso = forms.ModelChoiceField(
        label=_("Proceso Productivo: "),
        queryset=SubUnidadEconomicaPrincipalProceso.objects.all(), empty_label=_("Seleccione..."),
        widget=forms.Select(attrs={
            'placeholder':'Seleccione nombre proceso productivo',
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
                   'placeholder':'Ingrese nombre de la maquinaria',
                'class': 'form-control', 'data-toggle': 'tooltip', 'required': 'true',
                'title':_("Ingrese el nombre que posee la maquinaria o el equipo a registrar"),
                'style': 'width:200px',
            }
        )
    )
    ## País de origen de la maquinaria o el equipo
    pais_origen = forms.ChoiceField(
        label=_("País de Origen: "),
        choices=[('', 'Seleccione...')]+[(Pais.id, Pais.nombre) for Pais in Pais.objects.all()],
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
                'class': 'form-control input-md',
                'data-toggle': 'tooltip','title': _("Indique la descripción de la Maquinaria o Equipo"),
                'style': 'width:200px',
            })
    )

    EDO_ACTUAL =\
    (
    ('', _("Seleccione...")),
    ('Funcionamiento', _("En Fucionamiento")),
    ('Reparacion', _("En Reparacion")),
    ('Dañado', _("Dañado")),
)

    ## Estado de la maquinaria o el equipo
    estado_actual = forms.ChoiceField(
        label=_("Estado Actual: "),
        choices=EDO_ACTUAL,
        widget=forms.Select(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip', 'required': 'true',
                'title': _("Seleccione el estado actual de la Maquinario o Equipo"),
                'style': 'width:200px',
            }
        )
    )

    ## Año de Fabricacion
    date =forms.DateField(
        label=_("Año de Fabricación: "),
        widget=forms.DateInput(
            attrs={
                'class': 'datepicker', 'data-toggle': 'tooltip', 'required': 'true',
                'title':_("Seleccione el año de fabricacion de la Maquinaria o equipo"),
                'style': 'width:200px',
            }
        )
    )
    ## Vida Util
    vida_util = forms.IntegerField(
        label=_("Vida Util: "),
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip', 'required': 'true',
                'title':_("Seleccione los años de vida ultil de la Maquinaria o equipo"),
                'style': 'width:200px',
            }
        )
    )
    ## Año de Adquisicion
    date_adquisicion = forms.DateField(
        label=_("Año de adquisición: "),
        widget=forms.TextInput(
            attrs={
                'class': 'datepicker','data-toggle': 'tooltip', 'required': 'true',
                'title':_("Seleccione el año de Adquisicion de la Maquinaria o Equipo"),
                'style': 'width:200px',
            }
        )
    )

    class Meta:
        model = maquinariaModel
        fields = '__all__'
