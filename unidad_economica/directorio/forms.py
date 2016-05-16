"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.directorios.forms
#
# Contiene las clases, atributos y métodos para los formularios a implementar en el módulo de directorios
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>

from django import forms
from django.forms import (
    ModelForm, TextInput, Select, RadioSelect, ModelChoiceField)
from django.utils.translation import ugettext_lazy as _

from base.constant import (
    PREFIJO_DIRECTORIO_UNO_CHOICES, PREFIJO_DIRECTORIO_DOS_CHOICES, PREFIJO_DIRECTORIO_TRES_CHOICES,
    PREFIJO_DIRECTORIO_CUATRO_CHOICES
)
from base.models import Estado, Municipio, Parroquia
from base.fields import CoordenadaField
from .models import Directorio

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
    
    prefijo_uno = forms.ChoiceField(
        widget=RadioSelect(attrs={
            'class': 'radio'
        }), choices = PREFIJO_DIRECTORIO_UNO_CHOICES,
    )
    direccion_uno = forms.CharField(
        label=_("Dirección"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique el nombre"),
        })
    )
    prefijo_dos = forms.ChoiceField(
        widget=RadioSelect(attrs={
            'class': 'radio'
        }), choices = PREFIJO_DIRECTORIO_DOS_CHOICES,
    )
    direccion_dos = forms.CharField(
        label=_("Dirección"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique el nombre"),
        })
    )
    prefijo_tres = forms.ChoiceField(
        widget=RadioSelect(attrs={
            'class': 'radio',
        }), choices = PREFIJO_DIRECTORIO_TRES_CHOICES,
    )
    direccion_tres = forms.CharField(
        label=_("Dirección"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique el nombre"),
        }))
    prefijo_cuatro = forms.ChoiceField(
        widget=RadioSelect(attrs={
            'class': 'radio',
        }), choices = PREFIJO_DIRECTORIO_CUATRO_CHOICES,
    )
    direccion_cuatro = forms.CharField(
        label=_("Dirección"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique el nombre"),
    }))

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

    parroquia = ModelChoiceField(
        label=_("Parroquia"), queryset=Municipio.objects.all(), empty_label=_("Seleccione..."),
        widget=Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'disabled': 'true',
            'title': _("Seleccione la parroquia en donde se encuentra ubicada")
        })
    )

    coordenada = CoordenadaField()
    
    class Meta:
        model = Directorio
        exclude = ['activo']