"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidad_economica.#
# Formularios para la identificación de la unidad económica
# @author Eveli Ramírez (eramirez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 04-05-2016
# @version 2.0
from __future__ import unicode_literals
from django import forms
from django.forms import (
    ModelForm, ChoiceField, IntegerField, TextInput, CharField, Select)
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from base.constant import (
    PREFIJO_DIRECTORIO_UNO_CHOICES, PREFIJO_DIRECTORIO_DOS_CHOICES, PREFIJO_DIRECTORIO_TRES_CHOICES,
    PREFIJO_DIRECTORIO_CUATRO_CHOICES, SELECCION
)
from base.fields import RifField
from base.models import Pais, TipoComunal, Ciiu
from base.widgets import RifWidgetReadOnly
from .directorio.forms import DirectorioForm

from .models import UnidadEconomica

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

class UnidadEconomicaForm(DirectorioForm):
    """!
    Formulario para el registro de la unidad económica

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 04-05-2016
    @version 2.0
    """

    ## R.I.F. de la Unidad Económica que identifica al usuario en el sistema
    rif = RifField()
    rif.widget = RifWidgetReadOnly()

    ## Nombre Comercial de la Unidad Económica
    nombre_ue = CharField(
        label=_("Nombre Comercial: "),
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
                'title': _("Nombre Comercial de la Unidad Económica a registrar"), 'size': '50', 'readonly': 'readonly'
            }
        )
    )

    ## Razón Social
    razon_social = CharField(
        label=_("Razón Social: "),
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'readonly': 'readonly',
                'title': _("Razón Social"), 'size': '50',
            }
        )
    )

    ## Actividad económica principal
    actividad = ChoiceField(
        label=_("Actividad Económica Principal"),
        choices=[('','Seleccione...')]+[(actividad.codigo_ciiu, actividad.descripcion) for actividad in Ciiu.objects.all()],
        widget=Select(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Seleccione la Actividad Económica Principal que realiza")
            }
        )
    )

    ## Organización comunal
    orga_comunal = ChoiceField(
        label=_("¿Es una organización comunal?"),
        choices=SELECCION,
        widget=Select(attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("¿Es una organización comunal?"),
                'onchange': "habilitar(this.value, tipo_comunal.id), habilitar(this.value, situr.id)",
            }
        )
    )

    ## Tipo de organización comunal
    tipo_comunal = ChoiceField(
        label=_("Tipo de Organizacón Comunal: "),
        choices=[('', 'Seleccione...')]+[(comunal.id, comunal.tipo_comunal) for comunal in TipoComunal.objects.all()],
        widget=Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _("Seleccione el tipo de Organizacón Comunal"), 'disabled': 'disabled'
            }
        ), required=False
    )

    ## Código SITUR
    situr = CharField(
        label=_("Código SITUR:"),
        widget=TextInput(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
                'title': _("Código SITUR de la organización comunal"), 'size': '40', 'disabled': 'disabled'
            }
        ), required=False
    )

    ## Casa Matriz de alguna Franquicia
    casa_matriz_franquicia = ChoiceField(
        label=_("¿Es la casa matríz de una Franquicia?"),
        choices=SELECCION,
        widget=Select(attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("¿Es la casa matríz de una Franquicia?"),
                'onchange': "habilitar(this.value, nro_franquicia.id)",
            }
        )
    )

    ## Número de Franquicias asociadas a la Unidad Económica
    nro_franquicia = IntegerField(
        label=_("Número de Franquicias:"),
        initial=0,
        widget=TextInput(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
                'title': _("Número de Franquicias de la Unidad Económica"), 'size': '1', 'disabled': 'disabled' 
            }
        ), required=False
    )

    ## Franquiciado
    franquiciado = ChoiceField(
        label=_("¿Forma parte de una Franquicia?"),
        choices=SELECCION,
        widget=Select(attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("¿Forma parte de una Franquicia?"),
                'onchange': "habilitar(this.value, pais_franquicia.id), habilitar(this.value, nombre_franquicia.id), habilitar(this.value, rif_casa_matriz_0.id), habilitar(this.value, rif_casa_matriz_1.id, habilitar(this.value, rif_casa_matriz_2.id))",
            }
        )
    )

    ## País de la Franquicia
    pais_franquicia = ChoiceField(
        label=_("País de Origen de la Franquicia"),
        choices=[('', 'Seleccione...')]+[(pais.id, pais.nombre) for pais in Pais.objects.all()],
        widget=Select(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
                'title': _("Seleccione el país de origen de la franquicia"), 'disabled': 'disabled'
            }
        ), required=False
    )

    ## Nombre de la Franquicia
    nombre_franquicia = CharField(
        label=_("Nombre de la Franquicia"),
        widget=TextInput(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
                'title': _("Nombre de la franquicia"), 'size': '40', 'disabled': 'disabled'
            }
        ), required=False
    )

    ## RIF Franquicia
    rif_casa_matriz = RifField(disabled=True, required=False)

    def clean_nro_franquicia(self):
        nro_franquicia = self.cleaned_data.get('nro_franquicia')
        if nro_franquicia is None:
            return 0
            # above can be: return 1
            # but now it takes value from model definition
        else:
            return nro_franquicia

    def clean_tipo_comunal(self):
        tipo_comunal = self.cleaned_data['tipo_comunal']
        orga_comunal = self.cleaned_data['orga_comunal']

        if orga_comunal == 'S' and not tipo_comunal:
            raise forms.ValidationError(_("Seleccione un tipo de organización comunal"))

    class Meta(object):
        """docstring for Meta"""
        model = UnidadEconomica
        fields = ['rif', 'razon_social', 'nombre_ue']
            

