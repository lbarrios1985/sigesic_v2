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
    TextInput, CharField, Select, RadioSelect, Textarea, CheckboxInput
)
from unidad_economica.directorio.forms import DirectorioForm
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
from base.fields import RifField
from base.models import *
from base.constant import UNIDAD_MEDIDA
from base.widgets import RifWidgetReadOnly, RifWidget
from base.functions import cargar_actividad, cargar_pais
from .models import Producto, Cliente

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

CAPACIDAD_INSTALADA_MEDIDA = (('','Seleccione...'),("GR","Gramo"),("KG","Kilogramo"),("TN","Tonelada"))

@python_2_unicode_compatible
class BienesGeneralForm(forms.ModelForm):
    """!
    Clase que muestra el formulario de ingreso de la sub-unidad económica

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 13-07-2016
    @version 2.0.0
    """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(BienesGeneralForm, self).__init__(*args, **kwargs)
        self.fields['caev'].choices = cargar_actividad()
        self.fields['ubicacion_cliente'].choices = cargar_pais()
        #Se carga una lista con todas las subunidades relacionadas al usuario
        lista = [('','Selecione...')]
        for l in SubUnidadEconomica.objects.filter(rif=user.username).values_list('id','nombre_sub'):
            lista.append(l)
        self.fields['subunidad'].choices = lista
        #Se carga una lista con todos los productos relacionados a una subunidad
        prod = [('','Selecione...')]
        for p in Producto.objects.filter(subunidad_id__rif=user.username).values_list('id','nombre_producto'):
            prod.append(p)
        self.fields['cliente_producto'].choices = prod

    ## Listado de las subunidades disponibles
    subunidad =  forms.ChoiceField(
        label=_("Tipo de Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el Tipo de Sub-Unidad"),
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
        label=_("Número de Clientes"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de clientes"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )

    ## Cantidad de insumos
    cantidad_insumos = forms.CharField(
        label=_("Número de Insumos"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de insumos"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )
    
    ## Cantidad producida
    cantidad_produccion = forms.CharField(
        label=_("Producción"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de producción"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )
    
    ## Unidad de medida de la cantidad producida
    unidad_de_medida = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('','Seleccione...'),)+UNIDAD_MEDIDA, required = False,
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
    
    ## Lista con los productos
    cliente_producto = forms.ChoiceField(
        label=_("Producto"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el producto"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )
    
    ## Lista con los clientes del producto
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
    precio_venta = forms.CharField(
        label=_("Precio de venta por unidad"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio de venta por unidad"), 'size': '50',
            'style': 'width: 250px;',
        }),required = False,
    )
    
    ## Tipo de cambio
    tipo_cambio = forms.CharField(
        label=_("Tipo de cambio"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el tipo de cambio"), 'size': '50',
            'style': 'width: 250px;',
        }),required = False,
    )
    
    ## Cantidad producida
    cantidad_vendida = forms.CharField(
        label=_("Cantidades Vendidas"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de producción"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )
    
    ## Unidad de medida de la cantidad producida
    unidad_de_medida_cliente = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('','Seleccione...'),)+UNIDAD_MEDIDA, required = False,
    )
    
    class Meta:
        model = Producto
        fields = '__all__'
    
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
        self.fields['caev'].choices = cargar_actividad()
        self.fields['ubicacion_cliente'].choices = cargar_pais()
        #Se carga una lista con todas las subunidades relacionadas al usuario
        lista = [('','Selecione...')]
        for l in SubUnidadEconomica.objects.filter(rif=user.username).values_list('id','nombre_sub'):
            lista.append(l)
        self.fields['subunidad'].choices = lista
        #Se carga una lista con todos los productos relacionados a una subunidad
        prod = [('','Selecione...')]
        for p in Producto.objects.filter(subunidad_id__rif=user.username).values_list('id','nombre_producto'):
            prod.append(p)
        self.fields['cliente_producto'].choices = prod


    ## Listado de las subunidades disponibles
    subunidad =  forms.ChoiceField(
        label=_("Tipo de Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el Tipo de Sub-Unidad"),
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
        label=_("Número de Clientes"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de clientes"), 'size': '50', 'required':'required',
            'style': 'width: 250px;',
        }),
    )

    ## Cantidad de insumos
    cantidad_insumos = forms.CharField(
        label=_("Número de Insumos"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de insumos"), 'size': '50', 'required':'required',
            'style': 'width: 250px;',
        }),
    )
    
    ## Cantidad producida
    cantidad_produccion = forms.CharField(
        label=_("Producción"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de producción"), 'size': '50', 'required':'required',
            'style': 'width: 250px;',
        }),
    )
    
    ## Unidad de medida de la cantidad producida
    unidad_de_medida = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50', 'required':'required',
            'style': 'width: 250px;',
        }), choices = (('','Seleccione...'),)+UNIDAD_MEDIDA,
    )
    
    ## Listado del código caev
    caev = forms.ChoiceField(
        label=_("Código CAEV"),
        widget=Select(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Seleccione el código Caev"), 'required':'required',
            }
        ), choices = CaevClase.objects.values_list('clase','descripcion'),
    )
    
    ## Lista con los productos
    cliente_producto = forms.ChoiceField(
        label=_("Producto"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el producto"), 'size': '50',
            'style': 'width: 250px;',
        }),required = False,
    )
    
    ## Lista con los clientes del producto
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
    precio_venta = forms.CharField(
        label=_("Precio de venta por unidad"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio de venta por unidad"), 'size': '50',
            'style': 'width: 250px;',
        }),required = False,
    )
    
    ## Tipo de cambio
    tipo_cambio = forms.CharField(
        label=_("Tipo de cambio"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el tipo de cambio"), 'size': '50',
            'style': 'width: 250px;',
        }),required = False,
    )
    
    ## Cantidad producida
    cantidad_vendida = forms.CharField(
        label=_("Cantidades Vendidas"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de producción"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )
    
    ## Unidad de medida de la cantidad producida
    unidad_de_medida_cliente = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('','Seleccione...'),)+UNIDAD_MEDIDA, required = False,
    )
    
    class Meta:
        model = Producto
        exclude = ['subunidad','caev']
    

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
        self.fields['caev'].choices = cargar_actividad()
        self.fields['ubicacion_cliente'].choices = cargar_pais()
        #Se carga una lista con todas las subunidades relacionadas al usuario
        lista = [('','Selecione...')]
        for l in SubUnidadEconomica.objects.filter(rif=user.username).values_list('id','nombre_sub'):
            lista.append(l)
        self.fields['subunidad'].choices = lista
        #Se carga una lista con todos los productos relacionados a una subunidad
        prod = [('','Selecione...')]
        for p in Producto.objects.filter(subunidad_id__rif=user.username).values_list('id','nombre_producto'):
            prod.append(p)
        self.fields['cliente_producto'].choices = prod

     ## Listado de las subunidades disponibles
    subunidad =  forms.ChoiceField(
        label=_("Tipo de Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el Tipo de Sub-Unidad"),
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
        label=_("Número de Clientes"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de clientes"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )

    ## Cantidad de insumos
    cantidad_insumos = forms.CharField(
        label=_("Número de Insumos"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de insumos"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )
    
    ## Cantidad producida
    cantidad_produccion = forms.CharField(
        label=_("Producción"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de producción"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )
    
    ## Unidad de medida de la cantidad producida
    unidad_de_medida = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('','Seleccione...'),)+UNIDAD_MEDIDA, required = False,
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
    
    ## Lista con los productos
    cliente_producto = forms.ChoiceField(
        label=_("Producto"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el producto"), 'size': '50',
            'style': 'width: 250px;',
        }), 
    )
    
    ## Lista con los clientes del producto
    cliente_list = forms.ChoiceField(
        label=_("Cliente"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el cliente"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = [('','Seleccione...'), ("1","algo")],
    )
    
    ## Ubicación del cliente
    ubicacion_cliente = forms.ChoiceField(
        label=_("Ubicación del Cliente"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la ubicación del cliente"), 'size': '50',
            'style': 'width: 250px;',
        }),
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
        }),
    )
    
    ## Precio de venta
    precio_venta = forms.CharField(
        label=_("Precio de venta por unidad"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio de venta por unidad"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )
    
    ## Tipo de cambio
    tipo_cambio = forms.CharField(
        label=_("Tipo de cambio"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el tipo de cambio"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )
    
    ## Cantidad producida
    cantidad_vendida = forms.CharField(
        label=_("Cantidades Vendidas"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de producción"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )
    
    ## Unidad de medida de la cantidad producida
    unidad_de_medida_cliente = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('','Seleccione...'),)+UNIDAD_MEDIDA,
    )
    
    """def clean_rif(self):
        rif = self.cleaned_data['rif']
        ubicacion = self.cleaned_data['ubicacion_cliente']
        if((ubicacion == 'Venezuela') and (rif=='')):
            raise forms.ValidationError(_("Este campo es obligatorio"))
            rif.widget = RifWidget
        return rif"""
    
    class Meta:
        model = Cliente
        exclude = ['produccion','pais','nombre']
        