"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.coyuntura.forms
#
# Clases, atributos y métodos para los formularios de coyuntura
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
    TextInput, CharField, Select, RadioSelect, Textarea, CheckboxInput, NumberInput
)
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
from unidad_economica.models import UnidadEconomica
from base.fields import RifField
from base.widgets import RifWidget
from base.constant import UNIDAD_MEDIDA
from unidad_economica.bienes_prod_comer.models import Producto
from base.models import Cliente, AnhoRegistro, CaevClase, Estado
from base.functions import cargar_actividad, cargar_pais
from .models import *

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

LISTA_ANHO = (
    ('2016',_('2016')),
)

@python_2_unicode_compatible
class MesAdminForm(forms.ModelForm):
    """!
    Clase que muestra el formulario de ingreso del mes en la parte del administrador

    @author wpaez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 09-01-2017
    @version 2.0
    """

    def __init__(self, *args, **kwargs):
        super(MesAdminForm, self).__init__(*args, **kwargs)

    enero =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= ENERO,
    )

    febrero =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= FEBRERO,
    )

    marzo =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= MARZO,
    )

    abril =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= ABRIL,
    )

    mayo =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= MAYO,
    )

    junio =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= JUNIO,
    )

    julio =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= JULIO,
    )

    agosto =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= AGOSTO,
    )

    septiembre =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= SEPTIEMBRE,
    )

    octubre =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= OCTUBRE,
    )

    noviembre =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= NOVIEMBRE,
    )

    diciembre =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= DICIEMBRE,
    )

@python_2_unicode_compatible
class TrimestreAdminForm(forms.ModelForm):
    """!
    Clase que muestra el formulario de ingreso del trimestre en la parte del administrador

    @author wpaez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 09-01-2017
    @version 2.0
    """

    def __init__(self, *args, **kwargs):
        super(TrimestreAdminForm, self).__init__(*args, **kwargs)

    trimestre_1 =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= TRIMESTRE_1,
    )

    trimestre_2 =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= TRIMESTRE_2,
    )

    trimestre_3 =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= TRIMESTRE_3,
    )

    trimestre_4 =  forms.ChoiceField(
        widget=Select(attrs={
            'style': 'width: 150px;',
        }), required = False, choices= TRIMESTRE_4,
    )

@python_2_unicode_compatible
class PeriodicidadAdminForm(forms.ModelForm):
    """!
    Clase que muestra el formulario de ingreso de la periodicidad en la parte del administrador

    @author wpaez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 09-01-2017
    @version 2.0
    """

    def __init__(self, *args, **kwargs):
        super(PeriodicidadAdminForm, self).__init__(*args, **kwargs)

        #carga datos de PeriodoAdmin
        lista_mesadmin= [(None,'')]
        for lma in MesAdmin.objects.all():
            lista_mesadmin.append([lma.id,lma])
        self.fields['mes'].choices = lista_mesadmin

        #carga datos de PeriodoAdmin
        lista_trimestreadmin= [(None,'')]
        for lta in TrimestreAdmin.objects.all():
            lista_trimestreadmin.append([lta.id,lta])
        self.fields['trimestre'].choices = lista_trimestreadmin

        #carga datos de PeriodoAdmin
        lista_anhoadmin= [('','Seleccione...')]
        for laa in AnhoAdmin.objects.all():
            lista_anhoadmin.append([laa.id,laa])
        self.fields['anho'].choices = lista_anhoadmin

        #carga todas las actividades base_caevclase
        lista_caev= [(None,'')]
        for lc in CaevClase.objects.values_list('clase','descripcion'):
            lista_caev.append(lc)
        self.fields['caev'].choices = lista_caev

        #carga todas las unidades económicas
        lista_ue= [(None,'')]
        for lue in UnidadEconomica.objects.values_list('id','nombre_ue'):
            lista_ue.append(lue)
        self.fields['ue'].choices = lista_ue

        #carga todas las actividades base_caevclase
        lista_estado= [(None,'')]
        for le in Estado.objects.values_list('id','nombre'):
            lista_estado.append(le)
        self.fields['estado'].choices = lista_estado

        #carga datos de SubUnidadEconomica
        """lista_subunidad = [('','Selecione...')]
        for ls in SubUnidadEconomica.objects.exclude(tipo_sub_unidad="Se").values_list('id','nombre_sub'):
            lista_subunidad.append(ls)
        self.fields['sub_unidad_economica'].choices = lista_subunidad"""

    periodo =  forms.ChoiceField(
        label=_("Periodo"), widget=Select(attrs={
            'style': 'width: 150px;',
            'onchange': 'funcion_periodo(this.value);',
        }), choices= (('s','Seleccione...'),)+TIPO_PERIODICIDAD,
    )

    ## Establece algún mes
    mes =  forms.ChoiceField(
        label=_("Mes"), widget=Select(attrs={
            'style': 'width: 150px;',
            'data-toggle': 'tooltip','title': _("Seleccione un Mes"),
        }), required = False,
    )

    ## Establece algún trimestre
    trimestre =  forms.ChoiceField(
        label=_("Trimestre"), widget=Select(attrs={
            'style': 'width: 150px;',
            'data-toggle': 'tooltip','title': _("Seleccione el Trimestre"),
        }), required= False,
    )

    ## Establece algún año
    anho =  forms.ChoiceField(
        label=_("Año"), widget=Select(attrs={
            'style': 'width: 150px;',
            'data-toggle': 'tooltip','title': _("Seleccione un Año"),
        }),
    )

    tipo_consulta= forms.ChoiceField(
        label=_("Tipo de Consulta"), widget=Select(attrs={
            'style': 'width: 150px;','onchange': 'funcion_tipo_consulta(this.value);',
            'data-toggle': 'tooltip','title': _("Seleccione un Tipo"),
        }), choices= (('s','Seleccione...'),('caev','Por CAEV'),('ue','Por Unidad Económica'),('e','Por Estado'),),
    )

    caev= forms.ChoiceField(
        label=_("CAEV"), widget=Select(attrs={
            'style': 'width: 150px;',
            'data-toggle': 'tooltip','title': _("Seleccione una Actividad CAEV"),
        }), required= False,
    )

    ue= forms.ChoiceField(
        label=_("Unidad Economica"), widget=Select(attrs={
            'style': 'width: 150px;',
            'data-toggle': 'tooltip','title': _("Seleccione una Unidad Económica"),
        }), required= False,
    )

    estado= forms.ChoiceField(
        label=_("Estado"), widget=Select(attrs={
            'style': 'width: 150px;',
            'data-toggle': 'tooltip','title': _("Seleccione un Estado"),
        }), required= False,
    )

    def clean(self):
        cleaned_data = super(PeriodicidadAdminForm, self).clean()
        periodo= self.cleaned_data['periodo']
        mes= self.cleaned_data['mes']
        trimestre= self.cleaned_data['trimestre']
        tipo_consulta= self.cleaned_data['tipo_consulta']
        caev= self.cleaned_data['caev']
        ue= self.cleaned_data['ue']
        estado= self.cleaned_data['estado']

        ## agregué valor s al principio del select porque si esta '' la variable sale que no existe KeyError
        if periodo == 's':
            msg = "Este campo es obligatorio."
            self.add_error('periodo', msg)

        if mes == '' and trimestre == '':
            msg = "Ambos campos no pueden estar vacios."
            self.add_error('mes', msg)
            self.add_error('trimestre',msg)

        if caev == '' and ue == '' and estado == '':
            msg = "Los 3 campos no pueden estar vacios."
            self.add_error('caev', msg)
            self.add_error('ue', msg)
            self.add_error('estado', msg)

        if tipo_consulta == 's':
            msg = "Este campo es obligatorio."
            self.add_error('tipo_consulta', msg)

    class Meta:
        model = PeriodicidadAdmin
        exclude = ['mes','trimestre','anho','sub_unidad_economica']

@python_2_unicode_compatible
class ProduccionForm(forms.ModelForm):
    """!
    Clase que muestra el formulario de inicio de producción

    @author wpaez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 09-01-2017
    @version 2.0
    """

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProduccionForm, self).__init__(*args, **kwargs)
        self.fields['ubicacion_cliente'].choices = cargar_pais()

        ## Se carga una lista con todas las subunidades relacionadas al usuario
        ## ls: lista de subunidades temporal que se usa en el for
        lista_subunidad = [('','Selecione...')]
        for ls in SubUnidadEconomica.objects.filter(unidad_economica__user__username=user.username).exclude(tipo_sub_unidad="Se").values_list('id','nombre_sub'):
            lista_subunidad.append(ls)
        self.fields['sub_unidad_economica'].choices = lista_subunidad
        self.fields['sub_unidad_economica_cliente'].choices = lista_subunidad

        ## Se carga una lista con todos los productos relacionados a una subunidad
        ## lp: lista_producto temporal que se usa en el for
        lista_producto = [('','Selecione...')]
        for lp in Producto.objects.filter(subunidad__unidad_economica__user__username=user.username).values_list('id','nombre_producto'):
            lista_producto.append(lp)
        self.fields['producto'].choices = lista_producto

        ## Se carga una lista con todos los productos relacionados a la produccion
        ## se va creando la tupla lprod[(id de la Produccion),(con la clave foranea del producto se busca el nombre correspondiente)]
        lista_produccion= [('','Selecione...')]
        for lprod in Produccion.objects.values_list('id','producto'):
            lista_produccion.append([(lprod[0]),(Producto.objects.filter(pk=lprod[1]).get().nombre_producto)])
        self.fields['producto_cliente'].choices= lista_produccion

    ## esto es para periodicidad en la parte del usuario
    ## Establece el tipo de periodicidad
    periodo =  forms.ChoiceField(
        label=_("Periodo"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el periodo"),
            'style': 'width: 150px;', 'onchange': 'mostrar_ocultar(this.value);',
        }), choices = (('','Seleccione...'),)+TIPO_PERIODICIDAD,
    )

    ## Establece algún mes
    mes =  forms.ChoiceField(
        label=_("Mes"), widget=Select(attrs={
            'class': 'form-control input-md',
            'data-toggle': 'tooltip','title': _("Seleccione un Mes"),
            'style': 'width: 150px;', 'onchange': 'habilitar_deshabilitar_anho(this.value);',
        }), required = False, choices = (('','Seleccione...'),)+LISTA_MES,
    )

    ## Establece algún trimestre
    trimestre =  forms.ChoiceField(
        label=_("Trimestre"), widget=Select(attrs={
            'class': 'form-control input-md',
            'data-toggle': 'tooltip','title': _("Seleccione el Trimestre"),
            'style': 'width: 150px;', 'onchange': 'habilitar_deshabilitar_anho(this.value);',
        }), required= False, choices = (('','Seleccione...'),)+LISTA_TRIMESTRE,
    )

    ## Establece algún año
    anho =  forms.ChoiceField(
        label=_("Año"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione un Año"),
            'style': 'width: 150px;', 'disabled':'disabled', 'onchange': 'habilitar_deshabilitar_sub_unidad_economica(this.value);',
        }), choices = (('','Seleccione...'),)+LISTA_ANHO,
    )

    ## Listado de las subunidades disponibles
    sub_unidad_economica = forms.ChoiceField(
        label=_("Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione la Sub-Unidad"),
            'style': 'width: 250px;', 'disabled':'true',
            'onchange': "actualizar_combo(this.value,'bienes_prod_comer','Producto','subunidad','pk','nombre_producto','id_producto'),before_init_datatable('produccion_list','ajax/coyuntura-produccion-data','subunidad_id',$(this).val())",
        }),
    )

    ## Listado de los productos disponibles
    producto = forms.ChoiceField(
        label=_("Producto"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required',
            'data-toggle': 'tooltip','title': _("Seleccione el Producto"),
            'style': 'width: 250px;', 'disabled':'disabled',
        }),
    )

    ## cantidad producida
    cantidad_produccion = forms.CharField(
        label=_("Producción"), widget=NumberInput(attrs={
            'min': '1', 'step': 'any', 'class': 'form-control input-md', 'required':'required',
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
        label=_("Número de Clientes"), widget=NumberInput(attrs={
            'min': '1', 'class': 'form-control input-md', 'required':'required',
            'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de clientes"), 'size': '50',
            'style': 'width: 250px;',
        }),
    )

    ## Campos del formulario Clientes

    ## esto es para periodicidad en la parte del usuario
    ## Establece el tipo de periodicidad para clientes
    """periodo_cliente =  forms.ChoiceField(
        label=_("Periodicidad"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'disabled':'disabled',
            'data-toggle': 'tooltip','title': _("Indique la Periodicidad"),
            'style': 'width: 150px;',
        }), required = False,
    )

    ## Establece algún mes para clientes
    mes_cliente =  forms.ChoiceField(
        label=_("Mes"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'disabled':'disabled',
            'data-toggle': 'tooltip','title': _("Indique un Mes"),
            'style': 'width: 150px;',
        }), required = False,
    )

    ## Establece algún trimestre para clientes
    trimestre_cliente =  forms.ChoiceField(
        label=_("Trimestre"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'disabled':'disabled',
            'data-toggle': 'tooltip','title': _("Indique el Trimestre"),
            'style': 'width: 150px;',
        }), required = False,
    )

    ## Establece algún año para clientes
    anho_cliente =  forms.ChoiceField(
        label=_("Año"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'disabled':'disabled',
            'data-toggle': 'tooltip','title': _("Seleccione un Año"),
            'style': 'width: 150px;',
        }), required = False,
    )"""

    ## Listado de las subunidades disponibles
    sub_unidad_economica_cliente =  forms.ChoiceField(
        label=_("Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'style': 'width: 250px;',
            'data-toggle': 'tooltip','title': _("Seleccione la Sub-Unidad"),
            'onchange': "actualizar_combo(this.value,'coyuntura','Produccion','sub_unidad_economica_id','producto_id','producto','id_producto_cliente')",
        }), required = False,
    )

    ## Lista con los productos
    producto_cliente = forms.ChoiceField(
        label=_("Producto"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el producto"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange':"""
            habilitar(this.value, ubicacion_cliente.id),
            before_init_datatable("clientes_list","ajax/coyuntura-clientes-data","producto_id",$(this).val()),
            get_cliente_proveedor(this.value,"coyuntura","Produccion","producto_id","numero_clientes","#id_cliente_list","coyuntura","Clientes","produccion__producto_id","cliente")
            """,
        }), required = False,
    )

    ## Lista con los clientes del producto
    cliente_list = forms.CharField(
        label=_("Cliente"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el cliente"), 'size': '50',
            'style': 'width: 250px;', 'readonly':'readonly',
        }), required = False,
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
        }), required= False,
    )

    ## Precio de venta (Bs)
    precio_bs = forms.CharField(
        label=_("Precio de venta por unidad(bs)"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio de venta por unidad(bs)"), 'size': '50',
            'style': 'width: 250px;', 'min':'1', 'step':'any'
        }), required = False,
    )

    ## Precio de venta (Usd)
    precio_usd = forms.CharField(
        label=_("Precio de venta por unidad(usd)"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio de venta por unidad(usd)"), 'size': '50',
            'style': 'width: 250px;', 'min':'1', 'step':'any'
        }), required = False,
    )

    ## Cantidad producida
    cantidad_vendida = forms.CharField(
        label=_("Cantidades Vendidas"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de producción"), 'size': '50',
            'style': 'width: 250px;', 'min':'1',
        }), required = False,
    )

    ## Unidad de medida de la cantidad producida
    unidad_medida_cliente = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('','Seleccione...'),)+UNIDAD_MEDIDA, required = False,
    )

    def clean_periodicidad(self):
        periodo= self.cleaned_data['periodo']
        if periodo == '' :
            raise forms.ValidationError(_("Este campo es obligatorio."))
        return periodo

    def clean(self):
        cleaned_data = super(ProduccionForm, self).clean()
        mes= self.cleaned_data['mes']
        trimestre= self.cleaned_data['trimestre']

        if mes == '' and trimestre == '' :
            msg = "Debe seleccionar Mes o Trimestre, no ambos."
            self.add_error('mes', msg)
            self.add_error('trimestre', msg)

        if mes != '' and trimestre == '' :
            trimestre= None
        else:
            mes= None

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

    class Meta:
        model = Produccion
        exclude = ['sub_unidad_economica','producto','periodicidad']

@python_2_unicode_compatible
class ClientesForm(forms.ModelForm):
    """!
    Clase que muestra el formulario de inicio de clientes

    @author wpaez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 09-01-2017
    @version 2.0
    """

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ClientesForm, self).__init__(*args, **kwargs)
        self.fields['ubicacion_cliente'].choices = cargar_pais()

        ## Se carga una lista con todas las subunidades relacionadas al usuario
        ## ls: lista_subunidad temporal que se usa en el for
        lista_subunidad = [('','Selecione...')]
        for ls in SubUnidadEconomica.objects.filter(unidad_economica__user__username=user.username).exclude(tipo_sub_unidad="Se").values_list('id','nombre_sub'):
            lista_subunidad.append(ls)
        self.fields['sub_unidad_economica'].choices = lista_subunidad
        self.fields['sub_unidad_economica_cliente'].choices = lista_subunidad

        ## Se carga una lista con todos los productos relacionados a una subunidad
        ## lp: lista_producto temporal que se usa en el for
        lista_producto = [('','Selecione...')]
        for lp in Producto.objects.filter(subunidad__unidad_economica__user__username=user.username).values_list('id','nombre_producto'):
            lista_producto.append(lp)
        self.fields['producto'].choices = lista_producto

        ## Se carga una lista con todos los productos relacionados a la produccion
        ## se va creando la tupla lprod[(id de la Produccion),(con la clave foranea del producto se busca el nombre correspondiente)]
        lista_produccion= [('','Selecione...')]
        for lprod in Produccion.objects.values_list('id','producto'):
            lista_produccion.append([(lprod[0]),(Producto.objects.filter(pk=lprod[1]).get().nombre_producto)])
        self.fields['producto_cliente'].choices= lista_produccion

        ## Si se ha seleccionado una subunidad_cliente se elimina el atributo disabled
        if 'sub_unidad_economica_cliente' in self.data:
            self.fields['producto_cliente'].widget.attrs.pop('disabled')
            self.fields['ubicacion_cliente'].widget.attrs.pop('disabled')
            if (self.data['ubicacion_cliente']=='1'):
                self.fields['rif'].disabled = False
                self.fields['nombre_cliente'].widget.attrs['readonly'] = 'readonly'

    ## esto es para periodicidad en la parte del usuario
    ## Campos de Coyuntura-Produccion
    ## Establece el tipo de periodicidad
    periodo =  forms.ChoiceField(
        label=_("Periodo"), widget=Select(attrs={
            'class': 'form-control input-md',
            'data-toggle': 'tooltip','title': _("Seleccione el Periodo"),
            'style': 'width: 150px;', 'onchange': 'mostrar_ocultar(this.value);',
        }), choices = (('','Seleccione...'),)+TIPO_PERIODICIDAD, required= False,
    )

    ## Establece algún mes
    mes =  forms.ChoiceField(
        label=_("Mes"), widget=Select(attrs={
            'class': 'form-control input-md',
            'data-toggle': 'tooltip','title': _("Seleccione un Mes"),
            'style': 'width: 150px;', 'onchange': 'habilitar_deshabilitar_anho(this.value);',
        }), choices = (('','Seleccione...'),)+LISTA_MES, required= False,
    )

    ## Establece algún trimestre
    trimestre =  forms.ChoiceField(
        label=_("Trimestre"), widget=Select(attrs={
            'class': 'form-control input-md',
            'data-toggle': 'tooltip','title': _("Seleccione el Trimestre"),
            'style': 'width: 150px;', 'onchange': 'habilitar_deshabilitar_anho(this.value);',
        }), choices = (('','Seleccione...'),)+LISTA_TRIMESTRE, required= False,
    )

    ## Establece algún año
    anho =  forms.ChoiceField(
        label=_("Año"), widget=Select(attrs={
            'class': 'form-control input-md',
            'data-toggle': 'tooltip','title': _("Seleccione un Año"),
            'style': 'width: 150px;', 'disabled':'disabled', 'onchange': 'habilitar_deshabilitar_sub_unidad_economica(this.value);',
        }), choices = (('','Seleccione...'),)+LISTA_ANHO, required= False,
    )

    ## Listado de las subunidades disponibles
    sub_unidad_economica = forms.ChoiceField(
        label=_("Tipo de Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md',
            'data-toggle': 'tooltip','title': _("Seleccione el Tipo de Sub-Unidad"),
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange': "actualizar_combo(this.value,'bienes_prod_comer','Producto','subunidad','pk','nombre_producto','id_producto'),before_init_datatable('produccion_list','ajax/coyuntura-produccion-data','subunidad_id',$(this).val())",
        }), required= False,
    )

    ## Listado de los productos disponibles
    producto = forms.ChoiceField(
        label=_("Producto"), widget=Select(attrs={
            'class': 'form-control input-md',
            'data-toggle': 'tooltip','title': _("Seleccione el Producto"),
            'style': 'width: 250px;', 'disabled':'disabled',
        }), required= False,
    )

    ## cantidad producida
    cantidad_produccion = forms.CharField(
        label=_("Producción"), widget=NumberInput(attrs={
            'min': '1', 'step': 'any', 'class': 'form-control input-md',
            'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el valor de la producción"), 'size': '50',
            'style': 'width: 250px;',
        }), required= False,
    )

    ## Unidad de medida de la cantidad producida
    unidad_medida = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('','Seleccione...'),)+UNIDAD_MEDIDA, required= False,
    )

    ## Número de clientes
    numero_clientes = forms.CharField(
        label=_("Número de Clientes"), widget=NumberInput(attrs={
            'min': '1', 'class': 'form-control input-md',
            'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el número de clientes"), 'size': '50',
            'style': 'width: 250px;',
        }), required= False,
    )

    ## esto es para periodicidad en la parte del usuario
    ## Establece el tipo de periodicidad para clientes
    """periodo_cliente =  forms.ChoiceField(
        label=_("Periodicidad"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'disabled':'disabled', 'required': 'required',
            'data-toggle': 'tooltip','title': _("Indique la Periodicidad"),
            'style': 'width: 150px;',
        }), required= False,
    )

    ## Establece algún mes para clientes
    mes_cliente =  forms.ChoiceField(
        label=_("Mes"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'disabled':'disabled',
            'data-toggle': 'tooltip','title': _("Indique un Mes"),
            'style': 'width: 150px;',
        }), required = False,
    )

    ## Establece algún trimestre para clientes
    trimestre_cliente =  forms.ChoiceField(
        label=_("Trimestre"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'disabled':'disabled',
            'data-toggle': 'tooltip','title': _("Indique el Trimestre"),
            'style': 'width: 150px;',
        }), required = False,
    )

    ## Establece algún año para clientes
    anho_cliente =  forms.ChoiceField(
        label=_("Año"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'disabled':'disabled', 'required': 'required',
            'data-toggle': 'tooltip','title': _("Seleccione un Año"),
            'style': 'width: 150px;',
        }), required= False,
    )"""

    ## Listado de las subunidades disponibles
    sub_unidad_economica_cliente =  forms.ChoiceField(
        label=_("Sub-Unidad"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'width: 250px;',
            'data-toggle': 'tooltip','title': _("Seleccione el Tipo de Sub-Unidad"),
            'onchange': "actualizar_combo(this.value,'coyuntura','Produccion','sub_unidad_economica_id','producto_id','producto','id_producto_cliente')",
        }),
    )

    ## Lista con los productos
    producto_cliente = forms.ChoiceField(
        label=_("Producto"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el producto"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange':"""
            habilitar(this.value, ubicacion_cliente.id),
            before_init_datatable("clientes_list","ajax/coyuntura-clientes-data","producto_id",$(this).val()),
            get_cliente_proveedor(this.value,"coyuntura","Produccion","producto_id","numero_clientes","#id_cliente_list","coyuntura","Clientes","produccion__producto_id","cliente")
            """,
        }),
    )

    ## Lista con los clientes del producto
    cliente_list = forms.CharField(
        label=_("Cliente"), widget=TextInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione el cliente"), 'size': '50',
            'style': 'width: 250px;', 'readonly':'readonly',
        }), required = False,
    )

    ## Ubicación del cliente
    ubicacion_cliente = forms.ChoiceField(
        label=_("Ubicación del Cliente"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la ubicación del cliente"), 'size': '50',
            'style': 'width: 250px;', 'disabled':'disabled',
            'onchange':"""habilitar(this.value, rif_0.id),habilitar(this.value, rif_1.id),habilitar(this.value, rif_2.id),
            deshabilitar(this.value, nombre_cliente.id)""",
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
    precio_bs = forms.CharField(
        label=_("Precio de venta por unidad(bs)"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio de venta por unidad(bs)"), 'size': '50',
            'style': 'width: 250px;', 'min':'1','step':'any'
        }),
    )

    ## Precio de venta (Usd)
    precio_usd = forms.CharField(
        label=_("Precio de venta por unidad(usd)"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique el precio de venta por unidad(usd)"), 'size': '50',
            'style': 'width: 250px;', 'min':'1','step':'any'
        }),
    )

    ## Cantidad producida
    cantidad_vendida = forms.CharField(
        label=_("Cantidades Vendidas"), widget=NumberInput(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Indique la cantidad de producción"), 'size': '50',
            'style': 'width: 250px;', 'min':'1'
        }),
    )

    ## Unidad de medida de la cantidad producida
    unidad_medida_cliente = forms.ChoiceField(
        label=_("Unidad de Medida"), widget=Select(attrs={
            'class': 'form-control input-md', 'required':'required', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip','title': _("Seleccione la unidad de medida"), 'size': '50',
            'style': 'width: 250px;',
        }), choices = (('','Seleccione...'),)+UNIDAD_MEDIDA,
    )

    def clean_cliente_list(self):
        producto = self.cleaned_data['producto_cliente']
        cliente_list = self.cleaned_data['cliente_list']
        prod = Produccion.objects.filter(producto_id=producto).first()
        clientes = Clientes.objects.filter(produccion__producto_id=producto).all()
        if(prod.numero_clientes==len(clientes)):
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
        model = Clientes
        exclude = ['produccion', 'pais', 'cliente','cliente_list']

