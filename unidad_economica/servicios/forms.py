"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.servicios.forms
#
# Contiene las clases, atributos y métodos para los formularios a implementar en el módulo de servicios
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from django import forms
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.forms import (
    TextInput, CharField, Select, RadioSelect, Textarea, CheckboxInput
)
from unidad_economica.directorio.forms import DirectorioForm
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
from base.fields import RifField
from base.models import *
from base.constant import UNIDAD_MEDIDA, MONEDAS
from base.widgets import RifWidgetReadOnly, RifWidget
from base.functions import cargar_actividad, cargar_pais
from .models import Servicio, TipoServicio, ServicioCliente

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

CAPACIDAD_INSTALADA_MEDIDA = (('','Seleccione...'),("GR","Gramo"),("KG","Kilogramo"),("TN","Tonelada"))

@python_2_unicode_compatible
class ServiciosGeneralForm(forms.ModelForm):
    """!
    Clase que muestra el formulario de registro de servicios

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-08-2016
    @version 2.0.0
    """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ServiciosGeneralForm, self).__init__(*args, **kwargs)
        self.fields['caev'].choices = cargar_actividad()
        self.fields['ubicacion_cliente'].choices = cargar_pais()
        #Se carga una lista con todas las subunidades relacionadas al usuario
        lista = [('','Selecione...')]
        for l in SubUnidadEconomica.objects.filter(unidad_economica__user__username=user.username,sede_servicio=True).values_list('id','nombre_sub'):
            lista.append(l)
        self.fields['subunidad'].choices = lista

    ## Listado de las subunidades disponibles
    subunidad =  forms.ChoiceField(
        label=_("Tipo de Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required', 
            'data-toggle': 'tooltip','title': _("Seleccione el Tipo de Sub-Unidad"),
            'style': 'width: 250px;',
            'onchange':'before_init_datatable("servicios_list","ajax/servicios-data","subunidad_id",$(this).val())'
        }), required = False,
    )

    ## Nombre del servicio
    nombre_servicio = forms.CharField(
        label=_("Nombre del Servicio"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el nombre del servicio"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )
    
    ## Lista con los tipos de servicio
    tipo_servicio = forms.ChoiceField(
        label=_("Tipos de Servicios"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el tipo de servicio"), 'size': '50',
            'style': 'width: 250px;',
        }),required = False, choices = [('','Seleccione...'),(1,'algo')],#TipoServicio.objects.values_list('id','nombre'),
    )
        
    ## Cantidad de clientes
    cantidad_clientes =  forms.CharField(
        label=_("Número de Clientes"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de clientes"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )
    
    ## Listado del código caev
    caev = forms.ChoiceField(
        label=_("Código CAEV"),
        widget=Select(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Seleccione el código Caev"),
            }
        ), choices = CaevClase.objects.values_list('clase','descripcion'), required = False,
    )
    
    ## Lista con los servicios
    cliente_servicio = forms.ChoiceField(
        label=_("Servicio"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el servicio"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )
    
    ## Lista con los clientes del servicio
    cliente_list = forms.ChoiceField(
        label=_("Cliente"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el cliente"), 'size': '50',
            'style': 'width: 250px;',
        }),required = False, choices = [('','Seleccione...'), ("1","algo")],
    )
    
    ## Ubicación del cliente
    ubicacion_cliente = forms.ChoiceField(
        label=_("Ubicación del Cliente"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la ubicación del cliente"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )
    
    ## R.I.F. del cliente
    rif = RifField(required = False)
    rif.widget = RifWidgetReadOnly()
    
    ## Nombre del cliente
    nombre_cliente = forms.CharField(
        label=_("Nombre del Cliente"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el nombre del cliente"), 'size': '50',
            'style': 'width: 250px;',
        }),required = False,
    )
    
    ## Precio de venta
    precio = forms.CharField(
        label=_("Precio"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio"), 'size': '50',
            'style': 'width: 250px;',
        }),required = False,
    )
    
    ## Lista con los clientes del servicio
    tipo_moneda = forms.ChoiceField(
        widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la moneda"), 'size': '50',
            'style': 'width: 250px;',
        }),required = False, choices = MONEDAS,
    )
    
    ## Monto Facturado
    monto_facturado = forms.CharField(
        label=_("Monto Facturado"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el monto facturado"), 'size': '50',
            'style': 'width: 250px;',
        }),required = False,
    )
    
    ## Servicios prestados
    servicio_prestado = forms.CharField(
        label=_("Número de Servicios Prestados"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de servicios prestados"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )
    
    class Meta:
        model = Servicio
        fields = '__all__'