"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.directorio.forms
#
# Contiene las clases, atributos y métodos para los formularios a implementar en el módulo de directorios
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>

from django import forms
from django.forms import (
    ModelForm, TextInput, Select, RadioSelect, ModelChoiceField, HiddenInput, CharField
)
from django.utils.translation import ugettext_lazy as _

from base.constant import (
    PREFIJO_DIRECTORIO_UNO_CHOICES, PREFIJO_DIRECTORIO_DOS_CHOICES, PREFIJO_DIRECTORIO_TRES_CHOICES,
    PREFIJO_DIRECTORIO_CUATRO_CHOICES
)
from base.models import Estado, Municipio, Parroquia
from base.fields import CoordenadaField
from .models import TipoCoordenada, Directorio

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


class DirectorioForm(ModelForm):
    """!
    Clase que muestra el formulario de ingreso del directorio

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-05-2016
    @version 2.0.0
    """

    ## Prefijo para establecer el tipo de datos de la primera dirección
    tipo_vialidad = forms.ChoiceField(
        widget=RadioSelect(attrs={'class': 'radio'}), choices = PREFIJO_DIRECTORIO_UNO_CHOICES,
    )

    ## Primer dato correspondiente a la dirección de Autopista, Avenida, Carretera, Calle, Carrera o Vereda
    nombre_vialidad = forms.CharField(
        label=_("Dirección"), widget=TextInput(attrs={
            'class': 'form-control', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique el nombre"), 'placeholder': _('número o nombre')
        })
    )

    ## Prefijo para establecer el tipo de datos de la segunda dirección
    tipo_edificacion = forms.ChoiceField(
        widget=RadioSelect(attrs={'class': 'radio'}), choices = PREFIJO_DIRECTORIO_DOS_CHOICES,
    )

    ## Segundo dato correspondiente a la dirección de Edificio, Galpón, Quinta, Casa, Local o Centro Comercial
    descripcion_edificacion = forms.CharField(
        label='', widget=TextInput(attrs={
            'class': 'form-control', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique el nombre"), 'placeholder': _('número o nombre')
        })
    )

    ## Prefijo para establecer el tipo de datos de la tercera dirección
    tipo_subedificacion = forms.ChoiceField(
        widget=RadioSelect(attrs={'class': 'radio',}), choices = PREFIJO_DIRECTORIO_TRES_CHOICES
    )

    ## Tercer dato correspondiente a la dirección de Local, Oficina o Apartamento
    descripcion_subedificacion = forms.CharField(
        label='', widget=TextInput(attrs={
            'class': 'form-control input-sm', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique el nombre"), 'placeholder': _('número')
        })
    )

    ## Prefijo para establecer el tipo de datos de la cuarta dirección
    tipo_zonificacion = forms.ChoiceField(
        widget=RadioSelect(attrs={'class': 'radio',}), choices = PREFIJO_DIRECTORIO_CUATRO_CHOICES,
    )

    ## Cuarto dato correspondiente a la dirección de Urbanización, Sector o Zona
    nombre_zona = forms.CharField(
        label='', widget=TextInput(attrs={
            'class': 'form-control input-sm', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique el nombre"), 'placeholder': _('nombre')
        })
    )

    ## Estado o Entidad en donde se encuentra ubicado el municipio
    estado = ModelChoiceField(
        label=_("Estado"), queryset=Estado.objects.all(), empty_label=_("Seleccione..."),
        widget=Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'title': _("Seleccione el estado en donde se encuentra ubicada"),
            'onchange': "actualizar_combo(this.value,'base','Municipio','estado','pk','nombre','id_municipio')"
        })
    )

    ## Municipio en el que se encuentra ubicada la parroquia
    municipio = ModelChoiceField(
        label=_("Municipio"), queryset=Municipio.objects.all(), empty_label=_("Seleccione..."),
        widget=Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'disabled': 'true',
            'title': _("Seleccione el municipio en donde se encuentra ubicada"),
            'onchange': "actualizar_combo(this.value,'base','Parroquia','municipio','pk','nombre','id_parroquia')"
        })
    )

    ## Parroquia en donde se encuentra ubicada la dirección suministrada
    parroquia = ModelChoiceField(
        label=_("Parroquia"), queryset=Parroquia.objects.all(), empty_label=_("Seleccione..."),
        widget=Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'disabled': 'true',
            'title': _("Seleccione la parroquia en donde se encuentra ubicada")
        })
    )

    ## Tipos de coordenadas geográficas
    tipo_coordenada = ModelChoiceField(
        label=_("Tipo de Coordenada"), queryset=TipoCoordenada.objects.all(), empty_label=_("Seleccione..."),
        widget=Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'title': _("Seleccione el tipo de coordenada geográfica a registrar")
        }), required=False
    )

    ## Coordenadas geográficas de Longitud y Latitud
    coordenada = CoordenadaField(required=False)

    ## Id del directorio en haberse agregado una dirección existente
    directorio = CharField(widget=HiddenInput(attrs={'class': 'hide', 'readonly': 'readonly'}),required=False)
    
    class Meta:
        """!
        Metaclase que permite establecer las propiedades de la clase DirectorioForm

        @author Ing. Roldan Vargas rvargas at cenditel.gob.ve
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 23-06-2016
        @version 2.0.0
        """
        model = Directorio
        exclude = ['activo']

    def __init__(self, *args, **kwargs):
        """!
        Método que inicializa los atributos de la clase DirectorioForm

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 29-06-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param self <b>{*args}</b> Lista de argumentos del método
        @param self <b>{**kwargs}</b> Diccionario de argumentos del método
        """
        super(DirectorioForm, self).__init__(*args, **kwargs)

        # Si se ha seleccionado un estado establece el listado de municipios y elimina el atributo disable
        if 'estado' in self.data and self.data['estado']:
            self.fields['municipio'].widget.attrs.pop('disabled')
            self.fields['municipio'].queryset=Municipio.objects.filter(estado=self.data['estado'])

            # Si se ha seleccionado un municipio establece el listado de parroquias y elimina el atributo disable
            if 'municipio' in self.data and self.data['municipio']:
                self.fields['parroquia'].widget.attrs.pop('disabled')
                self.fields['parroquia'].queryset=Parroquia.objects.filter(municipio=self.data['municipio'])

        # Si se ha seleccionado un tipo de coordenada geográfica establece el atributo de coordenada como obligatorio
        if 'tipo_coordenada' in self.data and self.data['tipo_coordenada']:
            self.fields['coordenada'].required = True
