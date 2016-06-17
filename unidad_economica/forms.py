"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidad_economica.#
# Formularios para la identificación de la unidad económica
# @author Eveli Ramírez (eramirez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 04-05-2016
# @version 2.0
from __future__ import unicode_literals
from django import forms
from django.forms import (
    CharField, ChoiceField, IntegerField, Select, TextInput, CheckboxInput, NumberInput)
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from base.constant import (
    PREFIJO_DIRECTORIO_UNO_CHOICES, PREFIJO_DIRECTORIO_DOS_CHOICES, PREFIJO_DIRECTORIO_TRES_CHOICES,
    PREFIJO_DIRECTORIO_CUATRO_CHOICES, SELECCION
)
from base.fields import RifField
from base.models import Pais
from base.widgets import RifWidgetReadOnly
from base.functions import cargar_actividad, cargar_tipo_comunal

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
                'class': 'form-control', 'data-toggle': 'tooltip', 'size': '50',
                'title': _("Nombre Comercial de la Unidad Económica a registrar"), 'readonly': 'readonly'
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
        widget=Select(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Seleccione la Actividad Económica Principal que realiza")
            }
        )
    )

    ## Actividad económica secundaria
    actividad2 = ChoiceField(
        label=_("Actividad Económica Secundaria"),
        widget=Select(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
                'title': _("Seleccione la(s) Actividad(es) Economica(s) Secundaria(s) que realiza")
            }
        ), required=False
    )

    ## Actividad económica secundaria (datatable)
    actividad2_tb = forms.CharField(
        label=_("Actividad Económica Secundaria"),
        widget=Select(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
                'title': _("Seleccione la(s) Actividad(es) Economica(s) Secundaria(s) que realiza")
            }
        ), required=False
    )

    ## Organización comunal
    orga_comunal = ChoiceField(
        label=_("¿Es una organización comunal?"),
        choices=((True,''), (False,'')),
        widget=CheckboxInput(attrs={
                'class': 'seleccion_si_no', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("¿Es una organización comunal?"), 'value': 'S',
                'onchange': "habilitar($(this).is(':checked'), tipo_comunal.id), habilitar($(this).is(':checked'), situr.id)",
            }
        )
    )

    ## Tipo de organización comunal
    tipo_comunal = ChoiceField(
        label=_("Tipo de Organizacón Comunal: "),
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
        choices=((True,''), (False,'')),
        widget=CheckboxInput(attrs={
                'class': 'seleccion_si_no', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("¿Es la casa matríz de una Franquicia?"),
                'onchange': "habilitar($(this).is(':checked'), nro_franquicia.id)",
            }
        )
    )

    ## Número de Franquicias asociadas a la Unidad Económica
    nro_franquicia = CharField(
        label=_("Número de Franquicias:"),
        initial=0,
        widget=NumberInput(
            attrs={
                'class': 'form-control input-sm', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Número de Franquicias de la Unidad Económica"), 'size': '3', 'data-mask': '000',
                'disabled': 'disabled'
            }
        ), required=False
    )

    ## Franquiciado
    franquiciado = ChoiceField(
        label=_("¿Forma parte de una Franquicia?"),
        choices=((True,''), (False,'')),
        widget=CheckboxInput(attrs={
                'class': 'seleccion_si_no', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("¿Forma parte de una Franquicia?"),
                'onchange': "habilitar($(this).is(':checked'), pais_franquicia.id), habilitar($(this).is(':checked'), nombre_franquicia.id)",
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
                'title': _("Seleccione el país de origen de la franquicia"), 'disabled': 'disabled',
                'onchange': """habilitar(this.value, rif_casa_matriz_0.id),
                habilitar(this.value, rif_casa_matriz_1.id), habilitar(this.value, rif_casa_matriz_2.id), deshabilitar(this.value, nombre_franquicia.id)"""
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

    def __init__(self, *args, **kwargs):
        super(UnidadEconomicaForm, self).__init__(*args, **kwargs)
        self.fields['actividad'].choices = cargar_actividad()
        self.fields['actividad2'].choices = cargar_actividad()
        self.fields['tipo_comunal'].choices = cargar_tipo_comunal()

    def clean_nro_franquicia(self):
        casa_matriz_franquicia = self.cleaned_data.get('casa_matriz_franquicia')
        nro_franquicia = self.cleaned_data.get('nro_franquicia')
        if nro_franquicia is None:
            return 0
        else:
            return nro_franquicia

        print(casa_matriz_franquicia, nro_franquicia)

        if casa_matriz_franquicia == 'S' and nro_franquicia == '' or nro_franquicia == '0':
            raise forms.ValidationError(_("Indique el número de franquicias"))

    def clean_tipo_comunal(self):
        tipo_comunal = self.cleaned_data['tipo_comunal']

        if 'orga_comunal' in self.data:
            orga_comunal = self.data['orga_comunal']

            if orga_comunal == 'S' and not tipo_comunal:
                raise forms.ValidationError(_("Seleccione un tipo de organización comunal"))
            return orga_comunal

        return tipo_comunal

    def clean_situr(self):
        situr = self.cleaned_data['situr']

        if 'orga_comunal' in self.data:
            orga_comunal = self.data['orga_comunal']


            if orga_comunal == 'S' and not situr:
                raise forms.ValidationError(_("Indique el código SITUR de la organización comunal"))

        return situr

    def clean_pais_franquicia(self):
        franquiciado = self.cleaned_data['franquiciado']
        pais_franquicia = self.cleaned_data['pais_franquicia']

        if franquiciado == 'S' and not pais_franquicia:
            raise forms.ValidationError(_("Indique el país de origen de la franquicia"))
        return pais_franquicia

    def clean_rif_casa_matriz(self):
        rif_casa_matriz = self.cleaned_data['rif_casa_matriz']
        pais_franquicia = self.cleaned_data['pais_franquicia']

        if pais_franquicia == '1' and not rif_casa_matriz:
            raise forms.ValidationError(_("Indique el RIF de la franquicia"))
        return rif_casa_matriz

    def clean_nombre_franquicia(self):
        franquiciado = self.cleaned_data['franquiciado']
        nombre_franquicia = self.cleaned_data['nombre_franquicia']

        if franquiciado == 'S' and not nombre_franquicia:
            raise forms.ValidationError(_("Indique nombre de la franquicia"))
        return nombre_franquicia

    def clean_nro_franquicia(self):
        casa_matriz_franquicia = self.cleaned_data['casa_matriz_franquicia']
        nro_franquicia = self.cleaned_data['nro_franquicia']

        if casa_matriz_franquicia == 'S':
            raise forms.ValidationError(_("Indique número de franquicias"))
        return nro_franquicia

    class Meta(object):
        model = UnidadEconomica
        fields = ['rif', 'razon_social', 'nombre_ue']

