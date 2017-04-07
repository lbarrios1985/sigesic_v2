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
from django.utils.translation import ugettext_lazy as _
from base.models import Pais
from base.functions import cargar_pais
from base.constant import ESTADO_ACTUAL_MAQUINARIA, USO_ENERGIA
from .models import maquinariaModel
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica, SubUnidadEconomicaProceso

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

class MaquinariaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(MaquinariaForm, self).__init__(*args, **kwargs)
        ## Se cargan los paises
        self.fields['pais_origen'].choices = cargar_pais()
        #Se carga una lista con todas las subunidades relacionadas al usuario
        lista = [('','Selecione...')]
        for l in SubUnidadEconomica.objects.filter(unidad_economica__user__username=self.user.username).exclude(tipo_sub_unidad='Se').values_list('id','nombre_sub'):
            lista.append(l)
        self.fields['sub_unidad_economica'].choices = lista
        ## Se cargan los procesos de la subunidad
        procesos = [('','Selecione...')]
        for p in SubUnidadEconomicaProceso.objects.filter(sub_unidad_economica__unidad_economica__user__username=self.user.username).values_list('id','nombre_proceso'):
            procesos.append(p)
        self.fields['nombre_proceso'].choices = procesos
        
        # Si se ha seleccionado una sub_unidad_economica se elimina el atributo disabled del proceso
        if 'sub_unidad_economica' in self.data:
            self.fields['nombre_proceso'].widget.attrs.pop('disabled')
            

    ## nombre del proceso productivo extraido de registro de actividad economica
    sub_unidad_economica = forms.ChoiceField(
        label=_("Sub Unidad Economica"),
        widget=forms.Select(attrs={
            'placeholder':'Ingrese nombre de Sub unidad economica',
            'class': 'form-control', 'data-toggle': 'tooltip',
            'title':_(
                "Selecione el nombre de a sub unidad economica al que pertenece la maquinaria o el equipo a registrar"
            ),
            'onchange': """actualizar_combo(this.value,'sub_unidad_economica','SubUnidadEconomicaProceso','sub_unidad_economica',
                        'pk','nombre_proceso','id_nombre_proceso'),
                        before_init_datatable("maquinaria_list","ajax/maquinaria-data","subunidad_id",$(this).val())
                        """
        })
    )

    ## nombre del proceso productivo extraido de registro de actividad economica
    nombre_proceso = forms.ChoiceField(
        label=_("Proceso Productivo"),
        widget=forms.Select(attrs={
            'placeholder':'Seleccione nombre proceso productivo',
            'class': 'form-control', 'data-toggle': 'tooltip', 'disabled':'disabled',
            'title':_(
                "Selecione el nombre del proceso porductivo al que pertenece la maquinaria o el equipo a registrar"
            ),
            'onchange':"""
            mostrar_carga($(this).val(),'0000',"maquinaria_equipo","maquinariaModel","#carga_template_maquinaria")
            """
        })
    )

    ## Nombre de la maquinaria o el equipo
    nombre_maquinaria = forms.CharField(
        label=_("Nombre Maquinaria"),
        widget=forms.TextInput(
            attrs={
                'placeholder':'Ingrese nombre de la maquinaria',
                'class': 'form-control', 'data-toggle': 'tooltip',
                'title':_("Ingrese el nombre que posee la maquinaria o el equipo a registrar"),
            }
        )
    )
    ## País de origen de la maquinaria o el equipo
    pais_origen = forms.ChoiceField(
        label=_("País de Fabricación"),
        widget=forms.Select(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
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
            }
        )
    )

    ## Estado de la maquinaria o el equipo
    estado_actual = forms.ChoiceField(
        label=_("Estado Actual"), choices=(('','Seleccione...'),)+ESTADO_ACTUAL_MAQUINARIA,
        widget=forms.Select(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
                'title': _("Seleccione el estado actual de la Maquinario o Equipo"),
            }
        )
    )

    ## Año de Fabricacion
    anho_fabricacion =forms.IntegerField(
        label=_("Año de Fabricación"),
        widget=forms.TextInput(
            attrs={
                'class': 'datepicker form-control', 'data-toggle': 'tooltip', 'readonly': 'readonly',
                'title':_("Seleccione el año de fabricacion de la Maquinaria o equipo")
            }
        )
    )
    ## Vida Util
    vida_util = forms.IntegerField(
        label=_("Vida Util"),
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
                'title':_("Seleccione los años de vida ultil de la Maquinaria o equipo"),
            }
        )
    )
    ## Año de Adquisicion
    anho_adquisicion = forms.IntegerField(
        label=_("Año de adquisición"),
        widget=forms.TextInput(
            attrs={
                'class': 'datepicker form-control','data-toggle': 'tooltip', 'readonly': 'readonly',
                'title':_("Seleccione el año de Adquisicion de la Maquinaria o Equipo"),
            }
        )
    )
    
    ## País de origen de la maquinaria o el equipo
    uso_energia = forms.ChoiceField(
        label=_("Uso de Energía"),
        widget=forms.Select(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
                'title': _("Seleccione tipo de energía")
            }
        ), choices = (('',_('Seleccione...')),)+USO_ENERGIA,
    )

    class Meta:
        model = maquinariaModel
        exclude = ['proceso_sub_unidad']
