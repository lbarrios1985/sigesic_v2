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
    TextInput, Select,RadioSelect)
from django.utils.translation import ugettext_lazy as _

PREFIX1 = (("Autopista","Autopista"),("Avenida","Avenida"),("Carretera","Carretera"),
            ("Calle","Calle"),("Carrera","Carrera"),("Vereda","Vereda"))

PREFIX2 = (("Edificio","Edificio"),("Galpón","Galpón"),("Centro Comercial","Centro Comercial"),
            ("Quinta","Quinta"),("Casa","Casa"),("Local","Local"))

PREFIX3 = (("Local","Local"),("Oficina","Oficina"),("Apartamento","Apartamento"))

PREFIX4 = (("Urbanización","Urbanización"),("Sector","Sector"),("Zona","Zona"))

class DirectorioForm(forms.Form):
    """!
    Clase que muestra el formulario de ingreso del directorio

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-05-2016
    @version 2.0.0
    """
    
    prefijo1 = forms.ChoiceField(
        widget=RadioSelect(attrs={
            'style': 'min-width: 0; width: auto; display: inline;',
        }), choices = PREFIX1,
    )
    nombre1 = forms.CharField(
        label=_("Indique el nombre"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique el nombre"),
        })
    )
    prefijo2 = forms.ChoiceField(
        widget=RadioSelect(attrs={
            'style': 'min-width: 0; width: auto; display: inline;',
        }), choices = PREFIX2,
    )
    nombre2 = forms.CharField(
        label=_("Indique el nombre"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique el nombre"),
        })
    )
    prefijo3 = forms.ChoiceField(
        widget=RadioSelect(attrs={
            'style': 'min-width: 0; width: auto; display: inline;',
        }), choices = PREFIX3,
    )
    nombre3 = forms.CharField(
        label=_("Indique el nombre"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique el nombre"),
        }))
    prefijo4 = forms.ChoiceField(
        widget=RadioSelect(attrs={
            'style': 'min-width: 0; width: auto; display: inline;',
        }), choices = PREFIX4,
    )
    nombre4 = forms.CharField(
        label=_("Indique el nombre"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: 0; width: auto; display: inline;',
            'data-toggle': 'tooltip', 'title': _("Indique el nombre"),
    }))
    
    ## Entidad federal de la planta
    estado = forms.ChoiceField(
        label=_("Estado"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
        }), choices = ((1,"Mérida"),(2,"Caracas")),
    )
    
    ## Municipio de la planta
    municipio = forms.ChoiceField(
        label=_("Municipio"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
        }),
    )
    
    ## Parroquía de la planta
    parroquia = forms.ChoiceField(
        label=_("Parroquia"), widget=Select(attrs={
            'class': 'form-control input-md','style': 'min-width: 0; width: auto; display: inline;',
        }),
    )