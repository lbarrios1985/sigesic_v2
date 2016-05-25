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
from django import forms
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.forms import (
    TextInput, CharField, Select, RadioSelect, Textarea,
    )
from base.forms import TelefonoForm
from unidad_economica.directorio.forms import DirectorioForm
from .models import SubUnidadEconomica
from base.fields import RifField
from base.models import *
from base.widgets import RifWidgetReadOnly

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

CAPACIDAD_INSTALADA_MEDIDA = (('','Seleccione...'),("GR","Gramo"),("KG","Kilogramo"),("TN","Tonelada"))

TIPO_TENENCIA = (('','Seleccione...'),(1, "Ocupación"),(2,"Arrendada"),(3,"Comodato"),(4,"Propia"),(5,"Otra"))

TIPO_PROCESO = (('','Seleccione...'),("LN", "Lineas"),("ET","Estaciones de Trabajo"))

ESTADO_PROCESO = (('','Seleccione...'),(1, "Activo"),(0,"Inactivo"))


@python_2_unicode_compatible
class SubUnidadEconomicaForm(DirectorioForm,TelefonoForm):
    """!
    Clase que muestra el formulario de ingreso de la sub-unidad económica

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 04-05-2016
    @version 2.0.0
    """
    ## R.I.F. de la Unidad Económica que identifica al usuario en el sistema
    rif = RifField()
    rif.widget = RifWidgetReadOnly()

    ## Nombre de la sub unidad
    nombre_sub = forms.CharField(
        label=_("Nombre de la Sub-unidad"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el nombre"), 'size': '50', 'required':'required',
            'style': 'width: 250px;',
        })
    )
    
    ## Tipo de tenencia de la sub unidad
    tipo_tenencia = forms.ChoiceField(
        label=_("Tipo de Tenencia"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
        }),choices = TIPO_TENENCIA, 
    )
    
    ## Metros cuadrados de la construcción
    m2_contruccion = forms.DecimalField(
        label=_("Metros Cuadrados de la Construcción"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'data-rule-required': 'true', 'required':'required',
            'style': 'min-width: 0; width: auto; display: inline;', 'data-toggle': 'tooltip',
            'title': _("Indique lo metros cuadrados de la construcción"), 'size': '25', 'type':'number', 'step':'any',
        }),max_digits=20,decimal_places=5,
    )
    
    ## Metros cuadrados del terreno
    m2_terreno = forms.DecimalField(
        label=_("Metros Cuadrados de Terreno"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'data-rule-required': 'true', 'required':'required',
            'style': 'min-width: 0; width: auto; display: inline;', 'data-toggle': 'tooltip',
            'title': _("Indique lo metros cuadrados del terreno"), 'size': '25', 'type':'number', 'step':'any',
        }), max_digits=20,decimal_places=5,
    )
    
    ## Autonomía Eléctrica en porcentaje
    autonomia_electrica = forms.DecimalField(
        label=_("Porcentaje de Autonomía Eléctrica"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'data-rule-required': 'true', 'required':'required',
            'style': 'min-width: 0; width: auto; display: inline;', 'data-toggle': 'tooltip',
            'title': _("Indique la autonomía eléctrica en porcentaje"), 'size': '25', 'type':'number', 'step':'any',
        }), max_digits=20,decimal_places=5,
    )
    
    ## Consumo eléctrico promedio en el mes
    consumo_electrico = forms.DecimalField(
        label=_("Consumo Eléctrico"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'data-rule-required': 'true', 'required':'required',
            'style': 'min-width: 0; width: auto; display: inline;', 'data-toggle': 'tooltip',
            'title': _("Indique el consumo promedio mensual en Kw/h"), 'size': '25', 'type':'number', 'step':'any',
        }), max_digits=20,decimal_places=5,
    )
    
    cantidad_empleados = forms.IntegerField(
            label=_("Cantidad de empleados"), widget=TextInput(attrs={
            'class': 'form-control input-md','data-rule-required': 'true', 'required':'required',
            'style': 'min-width: 0; width: auto; display: inline;', 'data-toggle': 'tooltip',
            'title': _("Indique la cantidad de empleados"), 'size': '25', 'type':'number', 'min':'1',
        }),
    )
    
    ## Pregunta si la unidad económica presta un servicio
    sede_servicio =  forms.ChoiceField(
        label=_("Presta Servicio: "),
       widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'required':'required',
        }),choices = (('','Seleccione...'),(1,"Si"),(0,"No")),
    )
    
    class Meta:
        model = SubUnidadEconomica
        exclude = ['tipo_sub_unidad']
        
        
@python_2_unicode_compatible
class SubUnidadEconomicaActividadForm(SubUnidadEconomicaForm):
    """!
    Clase que muestra el formulario de ingreso de plantas productivas

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 16-05-2016
    @version 2.0.0
    """
    
    ## tipo de proceso productivo que se lleva a cabo en la sub unidad economica
    tipo_proceso = forms.ChoiceField(
        label=_("Tipo de Proceso Productivo"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el Tipo de Proceso Productivo"), 'size': '15',
        }), choices = TIPO_PROCESO, required=False,
    )
    
    ## nombre del proceso productivo
    nombre_proceso = forms.CharField(
        label=_("Nombre del Proceso Productivo"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el nombre"), 'size': '50',
        }), required=False,
    )
    
    ## descripcion del proceso productivo
    descripcion_proceso = forms.CharField(
        label=_("Descripción del Proceso Productivo"), widget=Textarea(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la descripción del proceso productivo"),
        }), required=False,
    )
    
    ## estado del proceso productivo
    estado_proceso = forms.ChoiceField(
        label=_("Estado del Proceso Productivo"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
        }), choices = ESTADO_PROCESO, required=False,
    )
    
    ## Código CIIU
    codigo_ciiu =  forms.ChoiceField(
        label=_("Actividad Económica Principal"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la Actividad Económica Principal"), 'size': '15',
            'required':'required',
        }), choices = [(1,"Primera Opcion"),(2,"Segunda Opcion")],
    )
    
    ## Capacidad instalada mensual (campo de texto)
    capacidad_instalada_texto = forms.DecimalField(
        label=_("Capacidad Instalada Mensual"), widget=TextInput(attrs={
            'class': 'form-control input-md','data-rule-required': 'true', 'required':'required',
            'style': 'min-width: 0; width: auto; display: inline;', 'data-toggle': 'tooltip',
            'title': _("Indique la capacidad instalada"), 'size': '25', 'type':'number', 'step':'any',
        }),max_digits=20,decimal_places=5,
    )
    
    ## Capacidad instalada mensual (Unidad de Medida)
    capacidad_instalada_medida = forms.ChoiceField(
        widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'required':'required',
        }), choices = CAPACIDAD_INSTALADA_MEDIDA,
    )
    
    ## Capacidad instalada mensual (campo de texto)
    capacidad_utilizada = forms.DecimalField(
        label=_("Capacidad Utilizada Mensual"), widget=TextInput(attrs={
            'class': 'form-control input-md','data-rule-required': 'true', 'required':'required',
            'style': 'min-width: 0; width: auto; display: inline;', 'data-toggle': 'tooltip',
            'title': _("Indique la capacidad utilizada en porcentaje"), 'size': '25', 'type':'number', 'step':'any',
        }),max_digits=20,decimal_places=5,
    )
    
@python_2_unicode_compatible
class SubUnidadEconomicaActividadTableForm(forms.Form):
    """!
    Clase que muestra el formulario de ingreso de plantas productivas

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 16-05-2016
    @version 2.0.0
    """
    
    ## tipo de proceso productivo que se lleva a cabo en la sub unidad economica
    tipo_proceso_tb = forms.CharField(
        label=_("Tipo de Proceso Productivo"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;', 'size': '30',
        }), 
    )
    
    ## nombre del proceso productivo
    nombre_proceso_tb = forms.CharField(
        label=_("Nombre del Proceso Productivo"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;','size': '30',
        }),
    )
    
    ## descripcion del proceso productivo
    descripcion_proceso_tb = forms.CharField(
        label=_("Descripción del Proceso Productivo"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;','size': '30',
        }),
    )
    
    ## estado del proceso productivo
    estado_proceso_tb = forms.CharField(
        label=_("Estado del Proceso Productivo"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;', 'size': '30',
        }),
    )