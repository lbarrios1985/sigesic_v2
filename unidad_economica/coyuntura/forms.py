"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.coyuntura.forms
#
# Clases, atributos y métodos para los formularios
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres 
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 22-09-2016
# @version 2.0
from django import forms
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.forms import (
    TextInput, CharField, Select, RadioSelect, Textarea, CheckboxInput
)
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
from base.constant import UNIDAD_MEDIDA, TIPO_PERIODICIDAD, LISTA_MES, LISTA_TRIMESTRE
from unidad_economica.bienes_prod_comer.models import Producto
from base.models import Cliente, AnhoRegistro
from .models import Produccion, Periodicidad
from base.functions import cargar_pais

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

LISTA_ANHO = (
    ('2014',_('2014')),
    ('2015',_('2015')),
    ('2016',_('2016')),
)

@python_2_unicode_compatible
class ProduccionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProduccionForm, self).__init__(*args, **kwargs)
        #self.fields['ubicacion_cliente'].choices = cargar_pais()

        #Se carga una lista con todas las subunidades relacionadas al usuario
        #ls: lista de subunidades temporal que se usa en el for
        lista_subunidad = [('','Selecione...')]
        for ls in SubUnidadEconomica.objects.filter(unidad_economica__user__username=user.username).values_list('id','nombre_sub'):
            lista_subunidad.append(ls)
        self.fields['sub_unidad_economica'].choices = lista_subunidad
        #Se carga una lista con todos los productos relacionados a una subunidad
        #lp: lista_producto temporal que se usa en el for
        lista_producto = [('','Selecione...')]
        for lp in Producto.objects.filter(subunidad__unidad_economica__user__username=user.username).values_list('id','nombre_producto'):
            lista_producto.append(lp)
        self.fields['producto'].choices = lista_producto

        """self.fields['producto'].choices = lista_producto
        #Se carga una lista con todos los clientes.
        #lc: lista_cliente temporal que se usa en el for
        lista_cliente = [('','Selecione...')]
        for lc in Cliente.objects.all().values_list('id','nombre'):
            lista_cliente.append(lc)
        self.fields['cliente'].choices = lista_cliente"""

    ##Establece el tipo de periodicidad
    periodicidad =  forms.ChoiceField(
        label=_("Periodicidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione la Periodicidad"),
            'style': 'width: 150px;', 'onchange': 'mostrar_ocultar(this.value);',
        }), choices = (('','Seleccione...'),)+TIPO_PERIODICIDAD,
    )

    ##Establece algun mes
    mes =  forms.ChoiceField(
        label=_("Mes"), widget=Select(attrs={
            'class': 'form-control input-md',
            'data-toggle': 'tooltip','title': _("Seleccione un Mes"),
            'style': 'width: 150px;', 'onchange': 'habilitar_deshabilitar_anho(this.value);',
        }), required = False, choices = (('','Seleccione...'),)+LISTA_MES,
    )

    ##Establece algun trimestre
    trimestre =  forms.ChoiceField(
        label=_("Trimestre"), widget=Select(attrs={
            'class': 'form-control input-md',
            'data-toggle': 'tooltip','title': _("Seleccione el Trimestre"),
            'style': 'width: 150px;', 'onchange': 'habilitar_deshabilitar_anho(this.value);',
        }), required= False, choices = (('','Seleccione...'),)+LISTA_TRIMESTRE,
    )

    ##Establece algun año
    anho =  forms.ChoiceField(
        label=_("Año"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione un Año"),
            'style': 'width: 150px;', 'disabled':'disabled', 'onchange': 'habilitar_deshabilitar_sub_unidad_economica(this.value);',
        }), choices = (('','Seleccione...'),)+LISTA_ANHO,
    )

    ## Listado de las subunidades disponibles
    sub_unidad_economica = forms.ChoiceField(
        label=_("Tipo de Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el Tipo de Sub-Unidad"),
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange': "actualizar_combo(this.value,'bienes_prod_comer','Producto','subunidad','pk','producto','id_producto'),before_init_datatable('produccion_list','ajax/coyuntura-produccion-data','subunidad_id',$(this).val())",
        }),
    )

    ## Listado de los productos disponibles
    producto = forms.ChoiceField(
        label=_("Seleccione un Producto"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el Producto"),
            'style': 'width: 250px;', 'disabled':'disabled',
        }),
    )

    ## cantidad producida
    cantidad_produccion = forms.CharField(
        label=_("Producción"), widget=TextInput(attrs={
            'type': 'number', 'min': '1', 'step': 'any', 'class': 'form-control input-md', 'required':'required',
            'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el valor de la producción"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )

    ## Unidad de medida de la cantidad producida
    unidad_medida = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('','Seleccione...'),)+UNIDAD_MEDIDA,
    )

    ## Número de clientes
    numero_clientes = forms.CharField(
        label=_("Número de Clientes"), widget=TextInput(attrs={
            'type': 'number','min': '1', 'class': 'form-control input-md', 'required':'required',
            'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de clientes"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )

    def clean_periodicidad(self):
        periodicidad= self.cleaned_data['periodicidad']
        if periodicidad == '' :
            raise forms.ValidationError(_("Este campo es obligatorio."))
        return periodicidad

    def clean_mes(self):
        mes= self.cleaned_data['mes']
        if mes == '' :
            mes= None
        return mes

    def clean_trimestre(self):
        trimestre= self.cleaned_data['trimestre']
        if trimestre == '' :
            trimestre= None
        return trimestre

    def clean_anho(self):
        anho= self.cleaned_data['anho']
        if anho == '' :
            raise forms.ValidationError(_("Este campo es obligatorio."))
        return anho

    def clean_sub_unidad_economica(self):
        sub_unidad_economica= self.cleaned_data['sub_unidad_economica']
        if sub_unidad_economica == '' :
            raise forms.ValidationError(_("Este campo es obligatorio."))
        return sub_unidad_economica

    def clean_producto(self):
        producto= self.cleaned_data['producto']
        if producto == '' :
            raise forms.ValidationError(_("Este campo es obligatorio."))
        return producto
    

    """## Precio en bolivares
    precio_bs = forms.CharField(
        label=_("Precio en Bolivares"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio en bolivares"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )

    ## Precio en dólares
    precio_usd = forms.CharField(
        label=_("Precio en Dólares"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio en dólares"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )

    ## Tipo de cambio nominal
    tipo_cambio_nominal = forms.CharField(
        label=_("Tipo de cambio nominal"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Tipo de cambio nominal"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )

    ## Cantidad de productos vendidos
    cantidad_vendida = forms.CharField(
        label=_("Cantidad vendida"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad vendida"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )

    ## Listado de clientes disponibles
    cliente = forms.ChoiceField(
        label=_("Seleccione un Cliente"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el Cliente"),
        }), required = False,
    )"""

    class Meta:
        model = Produccion
        exclude = ['sub_unidad_economica','producto','periodicidad']
        #fields = '__all__'

"""class CantidadClienteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CantidadClienteForm, self).__init__(*args, **kwargs)
        #self.fields['ubicacion_cliente'].choices = cargar_pais()

        #Se carga una lista con todas las subunidades relacionadas al usuario
        #ls: lista_subunidad temporal que se usa en el for
        lista_subunidad = [('','Selecione...')]
        for ls in SubUnidadEconomica.objects.filter(unidad_economica__user__username=user.username).values_list('id','nombre_sub'):
            lista_subunidad.append(ls)
        self.fields['sub_unidad_economica'].choices = lista_subunidad
        #Se carga una lista con todos los productos relacionados a una subunidad
        #lp: lista_producto temporal que se usa en el for
        lista_producto = [('','Selecione...')]
        for lp in Producto.objects.filter(subunidad__unidad_economica__user__username=user.username).values_list('id','nombre_producto'):
            lista_producto.append(lp)
        self.fields['producto'].choices = lista_producto
        #Se carga una lista con todos los clientes. lc: lista_cliente temporal que se usa en el for
        lista_cliente = [('','Selecione...')]
        for lc in Cliente.objects.all().values_list('id','nombre'):
            lista_cliente.append(lc)
        self.fields['cliente'].choices = lista_cliente

    ## Listado de las subunidades disponibles
    sub_unidad_economica = forms.ChoiceField(
        label=_("Tipo de Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el Tipo de Sub-Unidad"),
        }),required = False,
    )

    ## Listado de los productos disponibles
    producto = forms.ChoiceField(
        label=_("Seleccione un Producto"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el Producto"),
        }), required = False,
    )

    ## 
    produccion = forms.CharField(
        label=_("Producción"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el valor de la producción"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )

    ## Unidad de medida de la cantidad producida
    unidad_medida = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('','Seleccione...'),)+UNIDAD_MEDIDA, required = False,
    )

    ## Número de clientes
    numero_cliente = forms.CharField(
        label=_("Número de Clientes"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de clientes"), 'size': '50',
            'style': 'width: 250px;',
        }), required = False,
    )

    ## Precio en bolivares
    precio_bs = forms.CharField(
        label=_("Precio en Bolivares"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio en bolivares"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )

    ## Precio en dólares
    precio_usd = forms.CharField(
        label=_("Precio en Dólares"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio en dólares"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )

    ## Tipo de cambio nominal
    tipo_cambio_nominal = forms.CharField(
        label=_("Tipo de cambio nominal"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Tipo de cambio nominal"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )

    ## Cantidad de productos vendidos
    cantidad_vendida = forms.CharField(
        label=_("Cantidad vendida"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad vendida"), 'size': '50',
            'style': 'width: 250px;',
        })
    )

    ## Listado de clientes disponibles
    cliente = forms.ChoiceField(
        label=_("Seleccione un Cliente"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el Cliente"),
        }),
    )

    class Meta:
        model = CantidadCliente
        exclude = ['cliente']
        #fields = '__all__' """

