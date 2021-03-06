"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.bienes_prod_comer.forms
#
# Contiene las clases, atributos y métodos para los formularios a implementar en el módulo de bienes y productos comercializados
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
from base.widgets import RifWidget
from base.constant import UNIDAD_MEDIDA
from base.functions import cargar_pais, cargar_codigo_arancelario
from unidad_economica.utils import anho_pendiente, validar_anho
from .models import *

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

CAPACIDAD_INSTALADA_MEDIDA = (('','Seleccione...'),("GR","Gramo"),("KG","Kilogramo"),("TN","Tonelada"))
 
@python_2_unicode_compatible
class BienesForm(forms.ModelForm):
    """!
    Clase que muestra el formulario de ingreso de la sub-unidad económica

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 13-07-2016
    @version 2.0.0
    """
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        # now kwargs doesn't contain 'place_user', so we can safely pass it to the base class method
        super(BienesForm, self).__init__(*args, **kwargs)
        self.fields['codaran_subsubpartida'].choices = cargar_codigo_arancelario()
        self.fields['ubicacion_cliente'].choices = cargar_pais()
        self.fields['anho_registro'].choices = anho_pendiente(user.username)
        self.fields['anho'].choices = self.fields['anho_registro'].choices
        #Se carga una lista con todas las subunidades relacionadas al usuario
        lista = [('','Selecione...')]
        for l in SubUnidadEconomica.objects.filter(unidad_economica__user__username=user.username).exclude(tipo_sub_unidad="Se").values_list('id','nombre_sub'):
            lista.append(l)
        self.fields['subunidad'].choices = lista
        self.fields['subunidad_cliente'].choices = lista
        #Se carga una lista con todos los productos relacionados a una subunidad
        prod = [('','Selecione...')]
        for p in Producto.objects.filter(subunidad__unidad_economica__user__username=user.username).values_list('id','nombre_producto'):
            prod.append(p)
        self.fields['cliente_producto'].choices = prod
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
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el Año de Registro"), 'style': 'width: 250px;',
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
        label=_("Sub-unidad Económica"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el Tipo de Sub-Unidad"), 'style': 'width: 250px;',
            'onchange': """
            actualizar_combo(this.value,'bienes_prod_comer','Producto','subunidad','pk','nombre_producto','id_cliente_producto'),
            mostrar_carga_producto_cliente(this.value,$('#id_anho_registro option:selected').text(),"bienes_prod_comer","Produccion","#carga_template_produccion","#oculto_producto")
            """
            }),
    )

    ## Nombre del producto
    nombre_producto = forms.CharField(
        label=_("Nombre del Producto"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el nombre del producto"), 'size': '50', 'required':'required',
            'style': 'width: 250px;',
        }),
    )
    
    ## Especificación técnica del producto
    especificacion_tecnica = forms.CharField(
        label=_("Especificación Técnica"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la especificación técnica"), 'size': '50', 'required':'required',
            'style': 'width: 250px;',
        }),
    )
    
    ## Marca del producto
    marca = forms.CharField(
        label=_("Marca"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la marca"), 'size': '50', 'required':'required',
            'style': 'width: 250px;',
        }),
    )
    
    ## Cantidad de clientes
    cantidad_clientes =  forms.CharField(
        label=_("Número de Clientes"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de clientes"), 'size': '50', 'required':'required',
            'style': 'width: 250px;', 'step':'1'
        }),
    )

    ## Cantidad de insumos
    cantidad_insumos = forms.CharField(
        label=_("Número de Insumos"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de insumos"), 'size': '50', 'required':'required',
            'style': 'width: 250px;',
        }),
    )
    
    ## Cantidad producida
    cantidad_produccion = forms.CharField(
        label=_("Producción"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de producción"), 'size': '50', 'required':'required',
            'style': 'width: 250px;', 'step':'1'
        }),
    )
    
    ## Unidad de medida de la cantidad producida
    unidad_de_medida = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50', 'required':'required',
            'style': 'width: 250px;',
        }), choices = (('',_('Seleccione...')),)+UNIDAD_MEDIDA,
    )
    
    ## Listado del código arancelario
    codaran_subsubpartida = forms.ChoiceField(
        label=_("Código Arancelario"),
        widget=Select(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Seleccione el código Arancelario"), 'required':'required',
            }
        ),
    )
    
    ## Listado de las subunidades disponibles
    subunidad_cliente =  forms.ChoiceField(
        label=_("Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'width: 250px;',
            'data-toggle': 'tooltip','title': _("Seleccione el Tipo de Sub-Unidad"),
            'onchange': """
            actualizar_combo(this.value,'bienes_prod_comer','Producto','subunidad','pk','nombre_producto','id_cliente_producto'),
            mostrar_carga_producto_cliente(this.value,$('#id_anho_registro option:selected').text(),"bienes_prod_comer","FacturacionCliente","#carga_template_clientes","#oculto_cliente")
            """
        }),required = False,
    )
    
    ## Lista con los productos
    cliente_producto = forms.ChoiceField(
        label=_("Producto"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el producto"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange':"""
            habilitar(this.value, ubicacion_cliente.id),
            before_init_datatable("clientes_list","ajax/clientes-data","producto_id",$(this).val()),
            get_cliente_proveedor(this.value,"bienes_prod_comer","Produccion","producto_id","cantidad_clientes","#id_cliente_list","bienes_prod_comer","FacturacionCliente","produccion__producto_id","cliente")
            """
        }),required = False,
    )
    
    ## Lista con los clientes del producto
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
    
    ## Precio de venta (Bs)
    precio_venta_bs = forms.CharField(
        label=_("Precio de venta por unidad(bs)"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio de venta por unidad(bs)"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }),required = False,
    )
    
    ## Precio de venta (Usd)
    precio_venta_usd = forms.CharField(
        label=_("Precio de venta por unidad(usd)"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio de venta por unidad(usd)"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }),required = False,
    )
    
    ## Cantidad producida
    cantidad_vendida = forms.CharField(
        label=_("Cantidades Vendidas"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de producción"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }),required = False,
    )
    
    ## Unidad de medida de la cantidad producida
    unidad_de_medida_cliente = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('',_('Seleccione...')),)+UNIDAD_MEDIDA, required = False,
    )
    
    def clean(self):
        cleaned_data = super(BienesForm, self).clean()
        nombre_producto = self.cleaned_data['nombre_producto']
        anho_registro = self.cleaned_data['anho']
        subunidad = self.cleaned_data['subunidad']
        prod = Produccion.objects.filter(anho_registro_id=anho_registro,producto__subunidad_id=subunidad,producto__nombre_producto=nombre_producto)
        if(prod):
            msg =_("Ya registró la producción de ese producto en el año correspondiente")    
            self.add_error('nombre_producto', msg)
   
    class Meta:
        model = Producto
        exclude = ['subunidad','codaran_subsubpartida']
    

@python_2_unicode_compatible
class ClientesForm(forms.ModelForm):
    """!
    Clase que muestra el formulario de ingreso de la sub-unidad económica

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 13-07-2016
    @version 2.0.0
    """
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        # now kwargs doesn't contain 'place_user', so we can safely pass it to the base class method
        super(ClientesForm, self).__init__(*args, **kwargs)
        self.fields['codaran_subsubpartida'].choices = cargar_codigo_arancelario()
        self.fields['ubicacion_cliente'].choices = cargar_pais()
        #Se cargar el año de registro
        self.fields['anho_registro'].choices = anho_pendiente(user.username)
        self.fields['anho'].choices = self.fields['anho_registro'].choices
        #Se carga una lista con todas las subunidades relacionadas al usuario
        lista = [('','Selecione...')]
        for l in SubUnidadEconomica.objects.filter(unidad_economica__user__username=user.username).exclude(tipo_sub_unidad="Se").values_list('id','nombre_sub'):
            lista.append(l)
        self.fields['subunidad'].choices = lista
        self.fields['subunidad_cliente'].choices = lista
        #Se carga una lista con todos los productos relacionados a una subunidad
        prod = [('','Selecione...')]
        for p in Producto.objects.filter(subunidad__unidad_economica__user__username=user.username).values_list('id','nombre_producto'):
            prod.append(p)
        self.fields['cliente_producto'].choices = prod
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
            self.fields['cliente_producto'].widget.attrs.pop('disabled')
            self.fields['ubicacion_cliente'].widget.attrs.pop('disabled')
            if (self.data['ubicacion_cliente']=='1'):
                self.fields['rif'].disabled = False
                self.fields['nombre_cliente'].widget.attrs['readonly'] = 'readonly'

    ## Año registro
    anho_registro =  forms.ChoiceField(
        label=_("Año de Registro"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el Año de Registro"), 'style': 'width: 250px;',
            'onchange':'clone_value($(this).val(),"#id_anho")',
        }), required = False,
    )
    
    ## Año (para el campo anho_registro deshabilitado)
    anho =  forms.ChoiceField(
        widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto;',
            'data-toggle': 'tooltip', 'size': '50',
        }), required = False,
    )
    
    ## Listado de las subunidades disponibles
    subunidad =  forms.ChoiceField(
        label=_("Tipo de Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'width: 250px;',
            'data-toggle': 'tooltip','title': _("Seleccione el Tipo de Sub-Unidad"),
            'onchange':"""
            before_init_datatable("bienes_list","ajax/produccion-data","subunidad_id",$(this).val()),
            mostrar_carga_producto_cliente(this.value,$('#id_anho_registro option:selected').text(),"bienes_prod_comer","Produccion","#carga_template_produccion","#oculto_producto")
            """
        }), required = False,
    )

    ## Nombre del producto
    nombre_producto = forms.CharField(
        label=_("Nombre del Producto"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el nombre del producto"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )
    
    ## Especificación técnica del producto
    especificacion_tecnica = forms.CharField(
        label=_("Especificación Técnica"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la especificación técnica"), 'size': '50',
            'style': 'width: 250px;',
        }),required = False,
    )
    
    ## Marca del producto
    marca = forms.CharField(
        label=_("Marca"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la marca"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )
    
    ## Cantidad de clientes
    cantidad_clientes =  forms.CharField(
        label=_("Número de Clientes"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de clientes"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }), required = False,
    )

    ## Cantidad de insumos
    cantidad_insumos = forms.CharField(
        label=_("Número de Insumos"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de insumos"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }), required = False,
    )
    
    ## Cantidad producida
    cantidad_produccion = forms.CharField(
        label=_("Producción"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de producción"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }), required = False,
    )
    
    ## Unidad de medida de la cantidad producida
    unidad_de_medida = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('',_('Seleccione...')),)+UNIDAD_MEDIDA, required = False,
    )
    
    ## Listado del código Arancelario
    codaran_subsubpartida = forms.ChoiceField(
        label=_("Código Arancelario"),
        widget=Select(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Seleccione el código Arancelario"),
            }
        ), required = False,
    )
    
    ## Listado de las subunidades disponibles
    subunidad_cliente =  forms.ChoiceField(
        label=_("Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'width: 250px;',
            'data-toggle': 'tooltip','title': _("Seleccione el Tipo de Sub-Unidad"),
            'onchange': """
            actualizar_combo(this.value,'bienes_prod_comer','Producto','subunidad','pk','nombre_producto','id_cliente_producto'),
            mostrar_carga_producto_cliente(this.value,$('#id_anho_registro option:selected').text(),"bienes_prod_comer","FacturacionCliente","#carga_template_clientes","#oculto_cliente")
            """
        }),
    )
    
    ## Lista con los productos
    cliente_producto = forms.ChoiceField(
        label=_("Producto"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el producto"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange':"""
            habilitar(this.value, ubicacion_cliente.id),
            before_init_datatable("clientes_list","ajax/clientes-data","producto_id",$(this).val()),
            get_cliente_proveedor(this.value,"bienes_prod_comer","Produccion","producto_id","cantidad_clientes","#id_cliente_list","bienes_prod_comer","FacturacionCliente","produccion__producto_id","cliente")
            """
        }),
    )
    
    ## Lista con los clientes del producto
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
    
    ## Precio de venta (Bs)
    precio_venta_bs = forms.CharField(
        label=_("Precio de venta por unidad(bs)"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio de venta por unidad(bs)"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }),
    )
    
    ## Precio de venta (Usd)
    precio_venta_usd = forms.CharField(
        label=_("Precio de venta por unidad(usd)"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio de venta por unidad(usd)"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }),
    )
    
    ## Cantidad producida
    cantidad_vendida = forms.CharField(
        label=_("Cantidades Vendidas"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de producción"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }),
    )
    
    ## Unidad de medida de la cantidad producida
    unidad_de_medida_cliente = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('',_('Seleccione...')),)+UNIDAD_MEDIDA,
    )
    
    def clean_cliente_list(self):
        producto = self.cleaned_data['cliente_producto']
        cliente_list = self.cleaned_data['cliente_list']
        prod = Produccion.objects.filter(producto_id=producto).first()
        clientes = FacturacionCliente.objects.filter(produccion__producto_id=producto).all()
        if(prod.cantidad_clientes==len(clientes)):
            raise forms.ValidationError(_("No se pueden ingresar más clientes"))
        return cliente_list
  
    def clean(self):
        cleaned_data = super(ClientesForm, self).clean()
        rif = self.cleaned_data['rif']
        ubicacion_cliente = self.cleaned_data['ubicacion_cliente']
        if((ubicacion_cliente == '1') and (rif=='')):
            msg =_("Este campo es obligatorio")
            self.add_error('rif', msg)
    
    class Meta:
        model = FacturacionCliente
        exclude = ['produccion','pais','cliente','cliente_list']
        
