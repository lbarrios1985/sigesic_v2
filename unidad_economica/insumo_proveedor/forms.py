"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.insumo_proveedor.forms
#
# Contiene las clases, atributos y métodos para los formularios a implementar en el módulo de insumos y proveedores
# @author Hugo Ramirez (hramirez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 14-09-2016
# @version 2.0

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import (
    TextInput, CharField, Select, RadioSelect, Textarea, CheckboxInput, NumberInput, ChoiceField
)
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
from unidad_economica.bienes_prod_comer.models import Producto
from unidad_economica.utils import anho_pendiente, validar_anho
from .models import *
from base.fields import RifField
from base.models import *
from base.constant import UNIDAD_MEDIDA
from base.widgets import RifWidget
from base.functions import cargar_pais

class InsumoForm(forms.ModelForm):

    """!
    Clase para el formulario insumos proveedores

    @author Hugo Ramirez (hramirez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 14-09-2016
    @version 2.0.0
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(InsumoForm, self).__init__(*args, **kwargs)
        self.fields['pais_origen'].choices = cargar_pais()
        ## Se carga el año pendiente
        self.fields['anho_registro'].choices = anho_pendiente(self.user.username)
        self.fields['anho'].choices = self.fields['anho_registro'].choices
        #Se carga una lista con todas las subunidades relacionadas al usuario
        lista = [('','Selecione...')]
        for l in SubUnidadEconomica.objects.filter(unidad_economica__user__username=self.user.username).exclude(tipo_sub_unidad='Se').values_list('id','nombre_sub'):
            lista.append(l)
        self.fields['subunidad'].choices = lista
        self.fields['subunidad_insumo'].choices = lista
        #Se carga una lista con todos los productos relacionados a una subunidad
        prod = [('','Selecione...')]
        for p in Producto.objects.filter(subunidad__unidad_economica__user__username=self.user.username).values_list('id','nombre_producto'):
            prod.append(p)
        self.fields['producto'].choices = prod
        self.fields['producto_insumo'].choices = prod
        #Se carga una lista con todos los insumos relacionados a una subunidad
        insumo = [('','Selecione...')]
        for i in Insumo.objects.filter(producto__subunidad__unidad_economica__user__username=self.user.username).values_list('id','nombre_insumo'):
            insumo.append(i)
        self.fields['insumo'].choices = insumo
        #Se crea un arreglo con los años
        anhos = [item for item,key in self.fields['anho_registro'].choices if item!='']
        #Se definen los filtros
        filtros_prod = {'anho_registro_id__in':anhos,'producto__subunidad__unidad_economica__user__username':self.user.username}
        filtros_serv = {'anho_registro_id__in':anhos,'servicio__subunidad__unidad_economica__user__username':self.user.username}
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
            'disabled':'disabled'
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
    subunidad = forms.ChoiceField(
        label=_("Sub-Unidad Economica"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione Sub-Unidad Economica"), 'size': '50',
            'style': 'width: 250px;',
            'onchange':"""
            habilitar(this.value, producto.id),
            actualizar_combo(this.value,'bienes_prod_comer','Producto','subunidad','pk','nombre_producto','id_producto'),
            before_init_datatable("insumo_list","ajax/insumo-data","subunidad_id",$(this).val())
            """
        }),
    )
    
    ## Listado de los productos
    producto = forms.ChoiceField(
        label=_("Nombre del Producto"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el Producto"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled'
        }),
    )

    ## Nombre del insumo
    nombre_insumo = forms.CharField(
        label=_("Nombre del insumo"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el nombre del insumo"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )


    ## Especificación técnica del producto
    especificacion_tecnica = forms.CharField(
        label=_("Especificación Técnica"), widget=Textarea(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la especificación técnica"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )

    ## Marca del producto
    marca = forms.CharField(
        label=_("Marca"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la marca"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )

    ## Relacion insumo-proveedor
    relacion = forms.IntegerField(
        label=_("Relacion insumo-proveedor"), widget=NumberInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: o; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique la relacion insumo-proveedor"), 'size': '50',
            'style': 'width: 250px;',
        })
    )


    ## Numero de proveedores
    numero_proveedor = forms.IntegerField(
        label=_("Numero de proveedores"), widget=NumberInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: o; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique el numero de proveedores"), 'size': '50',
            'style': 'width: 250px;',
        })
    )
   
    ## Listado de las subunidades disponibles
    subunidad_insumo = forms.ChoiceField(
        label=_("Sub-Unidad Economica"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione Sub-Unidad Economica"), 'size': '50',
            'style': 'width: 250px;',
            'onchange':"""
            habilitar(this.value, producto_insumo.id),
            actualizar_combo(this.value,'bienes_prod_comer','Producto','subunidad','pk','nombre_producto','id_producto_insumo')
            """
        }), required=False
    )
    
    ## Listado de las subunidades disponibles
    producto_insumo = forms.ChoiceField(
        label=_("Producto"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione un Producto"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange':"""
            habilitar(this.value, insumo.id),
            actualizar_combo(this.value,'insumo_proveedor','Insumo','producto','pk','nombre_insumo','id_insumo')
            """
        }), required=False
    )

    ## Listado de insumos
    insumo = forms.ChoiceField(
        label=_("Insumo"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el insumo correspondiente al proveedor"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange':"""
            habilitar(this.value, pais_origen.id),
            before_init_datatable("proveedor_list","ajax/clientes-data","insumo_id",$(this).val()),
            get_cliente_proveedor(this.value,"insumo_proveedor","InsumoProduccion","insumo_id","numero_proveedor","#id_proveedor_list","InsumoProveedor","insumo_produccion__insumo_id","proveedor")
            """
        }), required=False
    )
    
    ## Lista con los proveedores del insumo
    proveedor_list = forms.CharField(
        label=_("Proveedor"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el proveedor"), 'size': '50',
            'style': 'width: 250px;', 'readonly':'readonly',
        }), required = False
    )
    
    ## Origen del insumo
    pais_origen = ChoiceField(
        label=_("País de origen: "), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione Sub-Unidad Economica"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange':"""habilitar(this.value, rif_0.id),habilitar(this.value, rif_1.id),habilitar(this.value, rif_2.id),
            deshabilitar(this.value, nombre_proveedor.id)"""
        }),required=False
    )

    ## R.I.F. del proveedor
    rif = RifField(disabled=True,required = False)


    ## Cantidad comprada
    cantidad_comprada = forms.CharField(
        label=_("Cantidades Comprada"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de Compra"), 'size': '50',
            'style': 'width: 250px;',
        }), required=False
    )

    ## Unidad de medida
    unidad_de_medida = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('','Seleccione...'),)+UNIDAD_MEDIDA, required=False
    )

    ## Nombre del insumo
    nombre_proveedor = forms.CharField(
        label=_("Nombre del proveedor"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el nombre del proveedor"), 'size': '50',
            'style': 'width: 250px;', 
        }), required=False
    )
    
    ## Precio de compra (Bs)
    precio_compra_bs = forms.CharField(
        label=_("Precio de compra por unidad(bs)"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio de compra por unidad(bs)"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }),required = False,
    )
    
    ## Precio de compra (Usd)
    precio_compra_usd = forms.CharField(
        label=_("Precio de compra por unidad(usd)"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio de compra por unidad(usd)"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }),required = False,
    )
    
    ## Cantidad comprada
    cantidad_comprada = forms.CharField(
        label=_("Cantidades Compradas"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de Compra"), 'size': '50',
            'style': 'width: 250px;',
        }), required=False
    )

    ## Unidad de medida
    unidad_de_medida = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('','Seleccione...'),)+UNIDAD_MEDIDA, required=False
    )



    class Meta:
        model = Insumo
        exclude = ['producto','subunidad']


class InsumoProveedorForm(forms.ModelForm):

    """!
    Clase para el formulario insumos proveedores

    @author Hugo Ramirez (hramirez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 14-09-2016
    @version 2.0.0
    """
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(InsumoProveedorForm, self).__init__(*args, **kwargs)
        self.fields['pais_origen'].choices = cargar_pais()
        ## Se carga el año pendiente
        self.fields['anho_registro'].choices = anho_pendiente(self.user.username)
        self.fields['anho'].choices = self.fields['anho_registro'].choices
        #Se carga una lista con todas las subunidades relacionadas al usuario
        lista = [('','Selecione...')]
        for l in SubUnidadEconomica.objects.filter(unidad_economica__user__username=self.user.username).exclude(tipo_sub_unidad='Se').values_list('id','nombre_sub'):
            lista.append(l)
        self.fields['subunidad'].choices = lista
        self.fields['subunidad_insumo'].choices = lista
        #Se carga una lista con todos los productos relacionados a una subunidad
        prod = [('','Selecione...')]
        for p in Producto.objects.filter(subunidad__unidad_economica__user__username=self.user.username).values_list('id','nombre_producto'):
            prod.append(p)
        self.fields['producto'].choices = prod
        self.fields['producto_insumo'].choices = prod
        #Se carga una lista con todos los insumos relacionados a una subunidad
        insumo = [('','Selecione...')]
        for i in Insumo.objects.filter(producto__subunidad__unidad_economica__user__username=self.user.username).values_list('id','nombre_insumo'):
            insumo.append(i)
        self.fields['insumo'].choices = insumo
        #Se crea un arreglo con los años
        anhos = [item for item,key in self.fields['anho_registro'].choices if item!='']
        #Se definen los filtros
        filtros_prod = {'anho_registro_id__in':anhos,'producto__subunidad__unidad_economica__user__username':self.user.username}
        filtros_serv = {'anho_registro_id__in':anhos,'servicio__subunidad__unidad_economica__user__username':self.user.username}
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
        if 'subunidad_insumo' in self.data:
            self.fields['producto_insumo'].widget.attrs.pop('disabled')
            self.fields['insumo'].widget.attrs.pop('disabled')
            self.fields['pais_origen'].widget.attrs.pop('disabled')
            if (self.data['pais_origen']=='1'):
                self.fields['rif'].disabled = False
                self.fields['nombre_proveedor'].widget.attrs['readonly'] = 'readonly'

    ## Año registro
    anho_registro =  forms.ChoiceField(
        label=_("Año de Registro"), widget=Select(attrs={
            'class': 'form-control input-md', 'data-toggle': 'tooltip',
            'title': _("Seleccione el Año de Registro"), 'style': 'width: 250px;',
            'disabled':'disabled'
        }), required=False
    )
    
    ## Año (para el campo anho_registro deshabilitado)
    anho =  forms.ChoiceField(
        widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto;',
            'data-toggle': 'tooltip', 'size': '50',
        }), required=False
    )
    
    ## Listado de las subunidades disponibles
    subunidad = forms.ChoiceField(
        label=_("Sub-Unidad Economica"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione Sub-Unidad Economica"), 'size': '50',
            'style': 'width: 250px;',
            'onchange':"""
            habilitar(this.value, producto.id),
            actualizar_combo(this.value,'bienes_prod_comer','Producto','subunidad','pk','nombre_producto','id_producto'),
            before_init_datatable("insumo_list","ajax/insumo-data","subunidad_id",$(this).val())
            """
        }), required=False
    )
    
    ## Listado de los productos
    producto = forms.ChoiceField(
        label=_("Nombre del Producto"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el Producto"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled'
        }), required=False
    )

    ## Nombre del insumo
    nombre_insumo = forms.CharField(
        label=_("Nombre del insumo"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el nombre del insumo"), 'size': '50',
            'style': 'width: 250px;',
        }),required=False
    )


    ## Especificación técnica del producto
    especificacion_tecnica = forms.CharField(
        label=_("Especificación Técnica"), widget=Textarea(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la especificación técnica"), 'size': '50',
            'style': 'width: 250px;',
        }),required=False
    )

    ## Marca del producto
    marca = forms.CharField(
        label=_("Marca"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la marca"), 'size': '50',
            'style': 'width: 250px;',
        }),required=False
    )

    ## Relacion insumo-proveedor
    relacion = forms.IntegerField(
        label=_("Relacion insumo-proveedor"), widget=NumberInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: o; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique la relacion insumo-proveedor"), 'size': '50',
            'style': 'width: 250px;',
        }),required=False
    )


    ## Numero de proveedores
    numero_proveedor = forms.IntegerField(
        label=_("Numero de proveedores"), widget=NumberInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: o; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique el numero de proveedores"), 'size': '50',
            'style': 'width: 250px;',
        }),required=False
    )
   
    ## Listado de las subunidades disponibles
    subunidad_insumo = forms.ChoiceField(
        label=_("Sub-Unidad Economica"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione Sub-Unidad Economica"), 'size': '50',
            'style': 'width: 250px;',
            'onchange':"""
            habilitar(this.value, producto_insumo.id),
            actualizar_combo(this.value,'bienes_prod_comer','Producto','subunidad','pk','nombre_producto','id_producto_insumo')
            """
        }),
    )
    
    ## Listado de las subunidades disponibles
    producto_insumo = forms.ChoiceField(
        label=_("Producto"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione un Producto"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange':"""
            habilitar(this.value, insumo.id),
            actualizar_combo(this.value,'insumo_proveedor','Insumo','producto','pk','nombre_insumo','id_insumo')
            """
        }),
    )

    ## Listado de insumos
    insumo = forms.ChoiceField(
        label=_("Insumo"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el insumo correspondiente al proveedor"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange':"""
            habilitar(this.value, pais_origen.id),
            before_init_datatable("proveedor_list","ajax/clientes-data","insumo_id",$(this).val()),
            get_cliente_proveedor(this.value,"insumo_proveedor","InsumoProduccion","insumo_id","numero_proveedor","#id_proveedor_list","InsumoProduccion","insumo_id","proveedor")
            """
        }),
    )
    
    ## Lista con los proveedores del insumo
    proveedor_list = forms.CharField(
        label=_("Proveedor"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el proveedor"), 'size': '50',
            'style': 'width: 250px;', 'readonly':'readonly',
        }),
    )
    
    ## Origen del insumo
    pais_origen = ChoiceField(
        label=_("País de origen: "), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione Sub-Unidad Economica"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange':"""habilitar(this.value, rif_0.id),habilitar(this.value, rif_1.id),habilitar(this.value, rif_2.id),
            deshabilitar(this.value, nombre_proveedor.id)"""
        }),
    )

    ## R.I.F. del proveedor
    rif = RifField(disabled=True)


    ## Cantidad comprada
    cantidad_comprada = forms.CharField(
        label=_("Cantidades Comprada"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de Compra"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )

    ## Unidad de medida
    unidad_de_medida = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('','Seleccione...'),)+UNIDAD_MEDIDA,
    )

    ## Nombre del insumo
    nombre_proveedor = forms.CharField(
        label=_("Nombre del proveedor"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el nombre del proveedor"), 'size': '50',
            'style': 'width: 250px;', 
        }),
    )
    
    ## Precio de compra (Bs)
    precio_compra_bs = forms.CharField(
        label=_("Precio de compra por unidad(bs)"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio de compra por unidad(bs)"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }),
    )
    
    ## Precio de compra (Usd)
    precio_compra_usd = forms.CharField(
        label=_("Precio de compra por unidad(usd)"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio de compra por unidad(usd)"), 'size': '50',
            'style': 'width: 250px;', 'step':'1'
        }),
    )
    
    ## Cantidad comprada
    cantidad_comprada = forms.CharField(
        label=_("Cantidades Compradas"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de Compra"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )

    ## Unidad de medida
    unidad_de_medida = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('','Seleccione...'),)+UNIDAD_MEDIDA,
    )

    class Meta:
        model = InsumoProveedor
        exclude = ['proveedor','insumo_produccion']
