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
    TextInput, CharField, Select, RadioSelect, Textarea, CheckboxInput, NumberInput
)
from unidad_economica.directorio.forms import DirectorioForm
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
from base.fields import RifField
from base.models import *
from base.constant import UNIDAD_MEDIDA, MONEDAS, TIPO_SERVICIO
from base.widgets import RifWidgetReadOnly, RifWidget
from base.functions import cargar_actividad, cargar_pais, cargar_anho
from .models import Servicio, ServicioCliente
from unidad_economica.bienes_prod_comer.models import Produccion
from unidad_economica.utils import anho_pendiente, validar_anho

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
        # Se carga el codigo caev, paises y años
        self.fields['caev'].choices = cargar_actividad()
        self.fields['ubicacion_cliente'].choices = cargar_pais()
        self.fields['anho_registro'].choices = anho_pendiente(user.username)
        self.fields['anho'].choices = self.fields['anho_registro'].choices
        #Se carga una lista con todas las subunidades relacionadas al usuario
        lista = [('','Selecione...')]
        for l in SubUnidadEconomica.objects.filter(unidad_economica__user__username=user.username,sede_servicio=True).values_list('id','nombre_sub'):
            lista.append(l)
        self.fields['subunidad'].choices = lista
        self.fields['subunidad_cliente'].choices = lista
        #Se carga una lista con todos los servicios relacionados a una subunidad
        serv = [('','Selecione...')]
        for s in Servicio.objects.filter(subunidad__unidad_economica__user__username=user.username).values_list('id','nombre_servicio'):
            serv.append(s)
        self.fields['cliente_servicio'].choices = serv
        #Se crea un arreglo con los años
        anhos = [item for item,key in self.fields['anho_registro'].choices if item!='']
        #Se definen los filtros
        filtros_prod = {'anho_registro_id__in':anhos,'producto__subunidad__unidad_economica__user__username':user.username}
        filtros_serv = {'anho_registro_id__in':anhos,'servicio__subunidad__unidad_economica__user__username':user.username}
        #Se obtiene la validacion por produccion
        validacion_prod = validar_anho('bienes_prod_comer','Produccion',**filtros_prod)
        #Se obtiene la validacion por servicios
        validacion_serv = validar_anho('servicios','ServicioCliente',**filtros_serv)
        #Si se cumple la validacion se llenan los campos con el valor y se deshabilitan
        if(validacion_prod['validacion']):
            self.fields['anho_registro'].widget.attrs = {'disabled':'disabled'}
            self.fields['anho_registro'].required = False
            self.initial['anho_registro'] = validacion_prod['anho_registro'].pk
            self.initial['anho'] = validacion_prod['anho_registro'].pk
        elif(validacion_serv['validacion']):
            self.fields['anho_registro'].widget.attrs = {'disabled':'disabled'}
            self.fields['anho_registro'].required = False
            self.initial['anho_registro'] = validacion_serv['anho_registro'].pk
            self.initial['anho'] = validacion_serv['anho_registro'].pk

    ## Año registro
    anho_registro =  forms.ChoiceField(
        label=_("Año de Registro"), widget=Select(attrs={
            'class': 'form-control input-md', 'data-toggle': 'tooltip',
            'title': _("Seleccione el Año de Registro"), 'style': 'width: 250px;',
            'onchange':'clone_value($(this).val(),"#id_anho")',
        }), required = False
    )
    
    ## Año (para el campo anho_registro deshabilitado)
    anho =  forms.ChoiceField(
        widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto;',
            'data-toggle': 'tooltip', 'size': '50',
        }), required = False
    )
    
    ## Listado de las subunidades disponibles
    subunidad =  forms.ChoiceField(
        label=_("Tipo de Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required', 
            'data-toggle': 'tooltip','title': _("Seleccione el Tipo de Sub-Unidad"),
            'style': 'width: 250px;',
            'onchange':"""
            before_init_datatable("servicios_list","ajax/servicios-data","subunidad_id",$(this).val()),
            mostrar_carga($(this).val(),$('#id_anho_registro option:selected').text(),"servicios","Servicio","#carga_template_servicios")
            """
        }),
    )

    ## Nombre del servicio
    nombre_servicio = forms.CharField(
        label=_("Nombre del Servicio"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el nombre del servicio"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )
    
    ## Lista con los tipos de servicio
    tipo_servicio = forms.ChoiceField(
        label=_("Tipos de Servicios"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el tipo de servicio"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('',_('Seleccione...')),)+TIPO_SERVICIO,
    )
        
    ## Cantidad de clientes
    cantidad_clientes =  forms.CharField(
        label=_("Número de Clientes"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de clientes"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }),
    )
    
    ## Listado del código caev
    caev = forms.ChoiceField(
        label=_("Código CAEV"),
        widget=Select(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Seleccione el código Caev"),
            }
        ),
    )
    
    ## Listado de las subunidades disponibles
    subunidad_cliente =  forms.ChoiceField(
        label=_("Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'width: 250px;',
            'data-toggle': 'tooltip','title': _("Seleccione el Tipo de Sub-Unidad"),
            'onchange': """
            actualizar_combo(this.value,'servicios','Servicio','subunidad','pk','nombre_servicio','id_cliente_servicio'),
            mostrar_carga($(this).val(),$('#id_anho_registro option:selected').text(),"servicios","ServicioCliente","#carga_template_clientes")
            """
        }),required = False,
    )
    
    ## Lista con los servicios
    cliente_servicio = forms.ChoiceField(
        label=_("Servicio"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el servicio"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange':"""
            habilitar(this.value, ubicacion_cliente.id),
            before_init_datatable("clientes_list","ajax/servicios-cliente-data","servicio_id",$(this).val()),
            get_cliente_proveedor(this.value,"servicios","Servicio","pk","cantidad_clientes","#id_cliente_list","ServicioCliente","servicio_id","cliente")
            """
        }), required = False,
    )
    
    ## Lista con los clientes del servicio
    cliente_list = forms.CharField(
        label=_("Cliente"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el cliente"), 'size': '50',
            'style': 'width: 250px;', 'readonly':'readonly',
        }), required = False
    )
    
    ## Ubicación del cliente
    ubicacion_cliente = forms.ChoiceField(
        label=_("Ubicación del Cliente"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la ubicación del cliente"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange':"""habilitar(this.value, rif_0.id),habilitar(this.value, rif_1.id),habilitar(this.value, rif_2.id),
            deshabilitar(this.value, nombre_cliente.id)"""
        }), required = False,
    )
    
    ## R.I.F. del cliente
    rif = RifField(disabled=True, required=False)
    
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
        label=_("Precio"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio"), 'size': '50',
            'style': 'width: 250px;', 'step':'0.1'
        }),required = False,
    )
    
    ## Lista con los clientes del servicio
    tipo_moneda = forms.ChoiceField(
        widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la moneda"), 'size': '50',
            'style': 'width: 250px;',
        }),required = False, choices = (('',_('Seleccione...')),) + MONEDAS,
    )
    
    ## Monto Facturado
    monto_facturado = forms.CharField(
        label=_("Monto Facturado"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el monto facturado"), 'size': '50',
            'style': 'width: 250px;', 'step':'0.1'
        }),required = False,
    )
    
    ## Servicios prestados
    servicio_prestado = forms.CharField(
        label=_("Número de Servicios Prestados"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de servicios prestados"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }), required = False,
    )
    
    class Meta:
        model = Servicio
        exclude = ['caev','subunidad']
        
@python_2_unicode_compatible
class ServiciosClienteForm(forms.ModelForm):
    """!
    Clase que muestra el formulario de registro de clientes de los servicios

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 24-10-2016
    @version 2.0.0
    """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ServiciosClienteForm, self).__init__(*args, **kwargs)
        # Se carga el codigo caev, paises y años
        self.fields['caev'].choices = cargar_actividad()
        self.fields['ubicacion_cliente'].choices = cargar_pais()
        # Se carga el año de registro
        self.fields['anho_registro'].choices = anho_pendiente(user.username)
        self.fields['anho'].choices = self.fields['anho_registro'].choices
        #Se carga una lista con todas las subunidades relacionadas al usuario
        lista = [('','Selecione...')]
        for l in SubUnidadEconomica.objects.filter(unidad_economica__user__username=user.username,sede_servicio=True).values_list('id','nombre_sub'):
            lista.append(l)
        self.fields['subunidad'].choices = lista
        self.fields['subunidad_cliente'].choices = lista
        #Se carga una lista con todos los servicios relacionados a una subunidad
        serv = [('','Selecione...')]
        for s in Servicio.objects.filter(subunidad__unidad_economica__user__username=user.username).values_list('id','nombre_servicio'):
            serv.append(s)
        self.fields['cliente_servicio'].choices = serv
        #Se crea un arreglo con los años
        anhos = [item for item,key in self.fields['anho_registro'].choices if item!='']
        #Se definen los filtros
        filtros_prod = {'anho_registro_id__in':anhos,'producto__subunidad__unidad_economica__user__username':user.username}
        filtros_serv = {'anho_registro_id__in':anhos,'servicio__subunidad__unidad_economica__user__username':user.username}
        #Se obtiene la validacion por produccion
        validacion_prod = validar_anho('bienes_prod_comer','Produccion',**filtros_prod)
        #Se obtiene la validacion por servicios
        validacion_serv = validar_anho('servicios','ServicioCliente',**filtros_serv)
        #Si se cumple la validacion se llenan los campos con el valor y se deshabilitan
        if(validacion_prod['validacion']):
            self.fields['anho_registro'].widget.attrs = {'disabled':'disabled'}
            self.fields['anho_registro'].required = False
            self.initial['anho_registro'] = validacion_prod['anho_registro'].pk
            self.initial['anho'] = validacion_prod['anho_registro'].pk
        elif(validacion_serv['validacion']):
            self.fields['anho_registro'].widget.attrs = {'disabled':'disabled'}
            self.fields['anho_registro'].required = False
            self.initial['anho_registro'] = validacion_serv['anho_registro'].pk
            self.initial['anho'] = validacion_serv['anho_registro'].pk
            
        # Si se ha seleccionado una subunidad_cliente se elimina el atributo disabled
        if 'subunidad_cliente' in self.data:
            self.fields['cliente_servicio'].widget.attrs.pop('disabled')
            self.fields['ubicacion_cliente'].widget.attrs.pop('disabled')
            if (self.data['ubicacion_cliente']=='1'):
                self.fields['rif'].disabled = False
                self.fields['nombre_cliente'].widget.attrs['readonly'] = 'readonly'
                    

    ## Año registro
    anho_registro =  forms.ChoiceField(
        label=_("Año de Registro"), widget=Select(attrs={
            'class': 'form-control input-md', 'data-toggle': 'tooltip',
            'title': _("Seleccione el Año de Registro"), 'style': 'width: 250px;',
            'onchange':'clone_value($(this).val(),"#id_anho")',
        }),
    )
    
    ## Año (para el campo anho_registro deshabilitado)
    anho =  forms.ChoiceField(
        widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto;',
            'data-toggle': 'tooltip', 'size': '50',
        }),
    )
    
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
        }),required = False, choices = (('',_('Seleccione...')),)+TIPO_SERVICIO,
    )
        
    ## Cantidad de clientes
    cantidad_clientes =  forms.CharField(
        label=_("Número de Clientes"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de clientes"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
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
        ), required = False,
    )
    
    ## Listado de las subunidades disponibles
    subunidad_cliente =  forms.ChoiceField(
        label=_("Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'width: 250px;',
            'data-toggle': 'tooltip','title': _("Seleccione el Tipo de Sub-Unidad"),
            'onchange': """
            actualizar_combo(this.value,'servicios','Servicio','subunidad','pk','nombre_servicio','id_cliente_servicio'),
            mostrar_carga($(this).val(),$('#id_anho_registro option:selected').text(),"servicios","ServicioCliente","#carga_template_clientes")
            """
        }),
    )
    
    ## Lista con los servicios
    cliente_servicio = forms.ChoiceField(
        label=_("Servicio"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el servicio"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange':"""
            habilitar(this.value, ubicacion_cliente.id),
            before_init_datatable("clientes_list","ajax/servicios-cliente-data","servicio_id",$(this).val()),
            get_cliente_proveedor(this.value,"servicios","Servicio","pk","cantidad_clientes","#id_cliente_list","ServicioCliente","servicio_id","cliente")
            """
        }),
    )
    
    ## Lista con los clientes del servicio
    cliente_list = forms.CharField(
        label=_("Cliente"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el cliente"), 'size': '50',
            'style': 'width: 250px;', 'readonly':'readonly',
        }),
    )
    
    ## Ubicación del cliente
    ubicacion_cliente = forms.ChoiceField(
        label=_("Ubicación del Cliente"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la ubicación del cliente"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange':"""habilitar(this.value, rif_0.id),habilitar(this.value, rif_1.id),habilitar(this.value, rif_2.id),
            deshabilitar(this.value, nombre_cliente.id)"""
        }),
    )
    
    ## R.I.F. del cliente
    rif = RifField(disabled=True, required=False)
    
    ## Nombre del cliente
    nombre_cliente = forms.CharField(
        label=_("Nombre del Cliente"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el nombre del cliente"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )
    
    ## Precio de venta
    precio = forms.CharField(
        label=_("Precio"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio"), 'size': '50',
            'style': 'width: 250px;', 'step':'0.1'
        }),
    )
    
    ## Lista con los clientes del servicio
    tipo_moneda = forms.ChoiceField(
        widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la moneda"), 'size': '50',
            'style': 'width: 250px;',
        }),choices = (('',_('Seleccione...')),) + MONEDAS,
    )
    
    ## Monto Facturado
    monto_facturado = forms.CharField(
        label=_("Monto Facturado"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el monto facturado"), 'size': '50',
            'style': 'width: 250px;', 'step':'0.1'
        }),
    )
    
    ## Servicios prestados
    servicio_prestado = forms.CharField(
        label=_("Número de Servicios Prestados"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de servicios prestados"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }),
    )
    
    def clean_cliente_list(self):
        servicio_cliente = self.cleaned_data['cliente_servicio']
        cliente_list = self.cleaned_data['cliente_list']
        servicio = Servicio.objects.get(pk=servicio_cliente)
        clientes = ServicioCliente.objects.filter(servicio_id=servicio_cliente).all()
        if(servicio.cantidad_clientes==len(clientes)):
            raise forms.ValidationError(_("No se pueden ingresar más clientes"))
        return cliente_list
    
    def clean(self):
        cleaned_data = super(ServiciosClienteForm, self).clean()
        rif = self.cleaned_data['rif']
        ubicacion_cliente = self.cleaned_data['ubicacion_cliente']
        if((ubicacion_cliente == '1') and (rif=='')):
            msg =_("Este campo es obligatorio")
            self.add_error('rif', msg)
    
    class Meta:
        model = ServicioCliente
        exclude = ['cliente','anho_registro','servicio']