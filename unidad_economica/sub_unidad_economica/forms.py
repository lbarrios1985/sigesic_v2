"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.sub_unidad_economica.forms
#
# Contiene las clases, atributos y métodos para los formularios a implementar en el módulo de sub unidades economicas
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import (
    TextInput, Select, Textarea, CheckboxInput, NumberInput
)
from django.core.validators import (
    MaxValueValidator, MinValueValidator
                                    )
from base.forms import TelefonoForm
from unidad_economica.directorio.forms import DirectorioForm
from .models import SubUnidadEconomica
from base.constant import TIPO_SUB_UNIDAD, TIPO_TENENCIA, ESTADO_PROCESO, TIPO_PROCESO, SERVICIOS_PUBLICOS
from base.fields import RifField
from base.models import *
from base.functions import cargar_actividad
from base.widgets import RifWidgetReadOnly

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

CAPACIDAD_INSTALADA_MEDIDA = (('','Seleccione...'),("GR","Gramo"),("KG","Kilogramo"),("TN","Tonelada"))

@python_2_unicode_compatible
class SubUnidadEconomicaForm(DirectorioForm, TelefonoForm):
    """!
    Clase que muestra el formulario de ingreso de la sub-unidad económica

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 04-05-2016
    @version 2.0.0
    """
    
    def __init__(self, *args, **kwargs):
        super(SubUnidadEconomicaForm, self).__init__(*args, **kwargs)

        self.fields['actividad_caev_primaria'].choices = cargar_actividad()
        self.fields['actividad_caev'].choices = cargar_actividad()
        self.fields['actividad_caev_tb'].choices = cargar_actividad()
        
    ## R.I.F. de la Unidad Económica que identifica al usuario en el sistema
    rif = RifField()
    rif.widget = RifWidgetReadOnly()

    ## Nombre de la sub unidad
    nombre_sub = forms.CharField(
        label=_("Nombre"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'data-toggle': 'tooltip','title': _("Indique el nombre"),
            'size': '50', 'required':'required'
        })
    )

    ## Tipo de tenencia de la sub unidad
    tipo_tenencia = forms.ChoiceField(
        label=_("Tipo de Tenencia"), widget=Select(attrs={'class': 'form-control select2', 'required':'required'}),
        choices = (('',_('Seleccione...')),) + TIPO_TENENCIA
    )

    ## Metros cuadrados de la construcción
    m2_construccion = forms.DecimalField(
        label=_("Metros Cuadrados de la Construcción"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'data-rule-required': 'true', 'required':'required',
            'data-toggle': 'tooltip', 'title': _("Indique lo metros cuadrados de la construcción"), 'size': '25',
            'onkeyup':'only_numbers_comma(this)',
        }), max_digits=20, decimal_places=5,
    )

    ## Metros cuadrados del terreno
    m2_terreno = forms.DecimalField(
        label=_("Metros Cuadrados de Terreno"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'data-rule-required': 'true', 'required':'required',
            'data-toggle': 'tooltip', 'title': _("Indique lo metros cuadrados del terreno"), 'size': '25',
            'onkeyup':'only_numbers_comma(this)',
        }), max_digits=20, decimal_places=5, validators = [MinValueValidator(1)]
    )

    ## Autonomía Eléctrica en porcentaje
    autonomia_electrica = forms.DecimalField(
        label=_("Autonomía Eléctrica (%)"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'data-rule-required': 'true', 'required':'required',
            'data-toggle': 'tooltip', 'title': _("Indique la autonomía eléctrica en porcentaje"), 'size': '25',
            'onkeyup':'only_numbers(this)',
        }), max_digits=20, decimal_places=5, validators = [MaxValueValidator(100),MinValueValidator(0)]
    )

    ## Consumo eléctrico promedio en el mes
    consumo_electrico = forms.DecimalField(
        label=_("Consumo Eléctrico Anual"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'data-rule-required': 'true', 'required':'required',
            'data-toggle': 'tooltip', 'title': _("Indique el consumo promedio anual en Kw"), 'size': '25',
            'onkeyup':'only_numbers(this)',
        }), max_digits=20, decimal_places=5,validators = [MinValueValidator(0)]
    )

    cantidad_empleados = forms.IntegerField(
        label=_("Número de trabajadores"), widget=TextInput(attrs={
            'class': 'form-control input-md','data-rule-required': 'true', 'required':'required',
            'data-toggle': 'tooltip', 'title': _("Indique el número de trabajadores"), 'size': '25',
            'onkeyup':'only_numbers(this)',
        }), validators = [MinValueValidator(1)]
    )
    
    servicios_publicos = forms.MultipleChoiceField(label = ('¿Cuenta con los siguientes Servicios Públicos?'),choices = SERVICIOS_PUBLICOS,
        widget=forms.CheckboxSelectMultiple(),required=False)

    ## Pregunta si la unidad económica presta un servicio
    sede_servicio =  forms.ChoiceField(
        label=_("Presta Servicio: "),
        widget=CheckboxInput(attrs={'class': 'seleccion_si_no',}),
        choices = ((True,'Si'), (False,'No')),
    )

    ## Tipo de Sub Unidad Económica
    tipo_sub_unidad = forms.ChoiceField(
        label=_("Uso"),
        widget=Select(attrs={'class': 'form-control input-md', 'required':'required'}),
        choices = (('',_('Seleccione...')),) + (TIPO_SUB_UNIDAD)
    )

    ## tipo de proceso productivo que se lleva a cabo en la sub unidad economica
    tipo_proceso = forms.ChoiceField(
        label=_("Tipo de Proceso Productivo"), widget=Select(attrs={
            'class': 'form-control input-md',
            'data-toggle': 'tooltip','title': _("Indique el Tipo de Proceso Productivo")
        }), choices = (('',_('Seleccione...')),)+ TIPO_PROCESO, required=False
    )

    ## nombre del proceso productivo
    nombre_proceso = forms.CharField(
        label=_("Nombre del Proceso Productivo"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'data-toggle': 'tooltip','title': _("Indique el nombre"), 'size': '50'
        }), required=False
    )

    ## descripcion del proceso productivo
    descripcion_proceso = forms.CharField(
        label=_("Descripción del Proceso Productivo"), widget=Textarea(attrs={
            'class': 'form-control input-md', 'data-toggle': 'tooltip',
            'title': _("Indique la descripción del proceso productivo")
        }), required=False
    )

    ## estado del proceso productivo
    estado_proceso = forms.ChoiceField(
        label=_("Estado del Proceso Productivo"), widget=Select(attrs={
            'class': 'form-control input-md', 'data-toggle': 'tooltip',
            'title': _("Indique el estado del proceso productivo")
        }), choices = (('',_('Seleccione...')),) + ESTADO_PROCESO, required=False
    )

    ## Código CAEV primaria
    actividad_caev_primaria =  forms.ChoiceField(
        label=_("Actividad Económica Primaria de la Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md',
            'data-toggle': 'tooltip','title': _("Indique la Actividad Económica Primaria de la Sub-Unidad en Ramas"),
            'onchange': 'deshabilitar_opcion(this.value,"#id_actividad_caev")'
        }), required=False
    )

    ## Código CAEV
    actividad_caev =  forms.ChoiceField(
        label=_("Actividad Económica Secundaria de la Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'data-toggle': 'tooltip',
            'title': _("Indique la Actividad Económica Secundaria de la Sub-Unidad en Ramas"),
            'onchange': 'deshabilitar_opcion(this.value,"#id_actividad_caev_tb")'
        }), required=False
    )

    ## Código CAEV
    actividad_caev_tb =  forms.ChoiceField(
        label=_("Actividad Económica de la Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'data-toggle': 'tooltip',
            'title': _("Indique la Actividad Económica de la Sub-Unidad en Ramas")
        }), required=False
    )

    ## Capacidad instalada mensual (campo de texto)
    capacidad_instalada_texto = forms.DecimalField(
        label=_("Capacidad Instalada"), widget=TextInput(attrs={
            'class': 'form-control input-md','data-rule-required': 'true',
            'data-toggle': 'tooltip', 'title': _("Indique la capacidad instalada"), 'size': '25',
            'onkeyup':'only_numbers_comma(this)',
        }), max_digits=20, decimal_places=5, required=False
    )
    
    ## Capacidad instalada mensual (Unidad de Medida)
    capacidad_instalada_medida = forms.ChoiceField(
        widget=Select(attrs={'class': 'form-control input-md'}),
        choices = CAPACIDAD_INSTALADA_MEDIDA,  required=False
    )

    ## Capacidad instalada mensual (campo de texto)
    capacidad_utilizada = forms.DecimalField(
        label=_("Capacidad Utilizada (%)"), widget=TextInput(attrs={
            'class': 'form-control input-md','data-rule-required': 'true',
            'data-toggle': 'tooltip', 'title': _("Indique la capacidad utilizada en porcentaje"), 'size': '25',
            'onkeyup':'only_numbers(this)',
        }), max_digits=20, decimal_places=5, required=False
    )

    ## tipo de proceso productivo que se lleva a cabo en la sub unidad economica (datatable)
    tipo_proceso_tb = forms.CharField(
        label=_("Tipo de Proceso Productivo"), widget=TextInput(attrs={'class': 'form-control input-md', 'size': '30'}),
        required=False
    )

    ## nombre del proceso productivo (datatable)
    nombre_proceso_tb = forms.CharField(
        label=_("Nombre del Proceso Productivo"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'size': '30'
        }), required=False
    )

    ## descripcion del proceso productivo (datatable)
    descripcion_proceso_tb = forms.CharField(
        label=_("Descripción del Proceso Productivo"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'size': '30'
        }), required=False
    )

    ## estado del proceso productivo (datatable)
    estado_proceso_tb = forms.CharField(
        label=_("Estado del Proceso Productivo"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'size': '30'
        }), required=False
    )

    def clean_codigo_ciiu(self):
        tipo = self.cleaned_data['tipo_sub_unidad']
        codigo_ciiu = self.cleaned_data['codigo_ciiu']

        if (tipo == 'Pl' or tipo == "Su") and codigo_ciiu=='':
            raise forms.ValidationError(_("Este campo es obligatorio"))

        return codigo_ciiu
        
    def clean_capacidad_instalada_texto(self):
        tipo = self.cleaned_data['tipo_sub_unidad']
        capacidad_instalada_texto = self.cleaned_data['capacidad_instalada_texto']

        if (tipo == 'Pl' or tipo == "Su") and not capacidad_instalada_texto:
            raise forms.ValidationError(_("Este campo es obligatorio"))

        return capacidad_instalada_texto
        
    def clean_capacidad_instalada_medida(self):
        tipo = self.cleaned_data['tipo_sub_unidad']
        capacidad_instalada_medida = self.cleaned_data['capacidad_instalada_medida']
        
        if (tipo == 'Pl' or tipo == "Su") and capacidad_instalada_medida=='':
            raise forms.ValidationError(_("Este campo es obligatorio"))

        return capacidad_instalada_medida
        
    def clean_capacidad_utilizada(self):
        tipo = self.cleaned_data['tipo_sub_unidad']
        capacidad_utilizada = self.cleaned_data['capacidad_utilizada']

        if (tipo == 'Pl' or tipo == "Su") and not capacidad_utilizada:
            raise forms.ValidationError(_("Este campo es obligatorio"))

        return capacidad_utilizada
    
    def clean_tipo_proceso_tb(self):
        tipo = self.cleaned_data['tipo_sub_unidad']
        tipo_proceso_tb = self.cleaned_data['tipo_proceso_tb']

        if tipo == 'Pl' and tipo_proceso_tb=='':
            raise forms.ValidationError(_("Este campo es obligatorio"))

        return tipo_proceso_tb
    
    def clean_nombre_proceso_tb(self):
        tipo = self.cleaned_data['tipo_sub_unidad']
        nombre_proceso_tb = self.cleaned_data['nombre_proceso_tb']

        if tipo == 'Pl' and nombre_proceso_tb=='':
            raise forms.ValidationError(_("Este campo es obligatorio"))

        return nombre_proceso_tb
    
    def clean_descripcion_proceso_tb(self):
        tipo = self.cleaned_data['tipo_sub_unidad']
        descripcion_proceso_tb = self.cleaned_data['descripcion_proceso_tb']

        if tipo == 'Pl' and descripcion_proceso_tb=='':
            raise forms.ValidationError(_("Este campo es obligatorio"))

        return descripcion_proceso_tb
    
    def clean_estado_proceso_tb(self):
        tipo = self.cleaned_data['tipo_sub_unidad']
        estado_proceso_tb = self.cleaned_data['estado_proceso_tb']

        if tipo == 'Pl' and estado_proceso_tb=='':
            raise forms.ValidationError(_("Este campo es obligatorio"))

        return estado_proceso_tb
    
    def clean_actividad_caev_primaria(self):
        tipo = self.cleaned_data['tipo_sub_unidad']
        actividad_caev_primaria = self.cleaned_data['actividad_caev_primaria']

        if (tipo == 'Pl' or tipo == "Su") and actividad_caev_primaria=='':
            raise forms.ValidationError(_("Este campo es obligatorio"))

        return actividad_caev_primaria
    
    def clean_m2_construccion(self):
        construccion = self.cleaned_data['m2_construccion']
        if construccion < 1:
            raise forms.ValidationError(_("Asegúrese de que este valor es mayor o igual a 1."))

        return construccion
    
    def clean_m2_terreno(self):
        terreno = self.cleaned_data['m2_terreno']
        construccion = self.cleaned_data['m2_construccion']

        if terreno < construccion:
            raise forms.ValidationError(_("Los metros del terreno no pueden ser menores que la construcción"))

        return terreno
    
    def clean_capacidad_utilizada(self):
        capacidad = self.cleaned_data['capacidad_utilizada']
        tipo = self.cleaned_data['tipo_sub_unidad']
        if (tipo == 'Pl' or tipo == "Su"):
            if capacidad < 0:
                raise forms.ValidationError(_("Asegúrese de que este valor es mayor o igual a 0."))
            elif capacidad > 100:
                raise forms.ValidationError(_("Asegúrese de que este valor es menor o igual a 100."))
        return capacidad
    
    class Meta:
        model = SubUnidadEconomica
        exclude = ['unidad_economica']
