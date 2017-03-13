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
from base.widgets import RifWidgetReadOnly, RifWidget
from base.functions import cargar_actividad, cargar_tipo_comunal, cargar_pais

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
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UnidadEconomicaForm, self).__init__(*args, **kwargs)

        self.fields['actividad'].choices = cargar_actividad()
        self.fields['actividad2'].choices = cargar_actividad()

        # Si se ha indicado que es una organizacion comunal, se habilitan los atributos tipo_comunal y situr
        if 'orga_comunal' in self.data:
            self.fields['tipo_comunal'].widget.attrs.pop('disabled')
            self.fields['situr'].widget.attrs.pop('readonly')

        self.fields['tipo_comunal'].choices = cargar_tipo_comunal()

        if 'casa_matriz_franquicia' in self.data:
            self.fields['nro_franquicia'].widget.attrs.pop('readonly')
            #self.fields['franquiciado'].widget.attrs.pop('readonly')

        if 'franquiciado' in self.data:
            self.fields['pais_franquicia'].widget.attrs.pop('disabled')
            if 'pais_franquicia' in self.data and self.data['pais_franquicia']:
                self.fields['rif_casa_matriz'].disabled=False
            else:
                self.fields['nombre_franquicia'].widget.attrs.pop('readonly')


        self.fields['pais_franquicia'].choices = cargar_pais()

    ## R.I.F. de la Unidad Económica que identifica al usuario en el sistema
    rif = RifField()
    rif.widget = RifWidgetReadOnly()

    ## Nombre Comercial de la Unidad Económica
    nombre_ue = CharField(
        label=_("Nombre Comercial: "),
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

    ## La unidad Económica es exportador (si o no)
    exportador = ChoiceField(
        label=_("¿Es Exportador?"),
        choices=((True,''), (False,'')),
        widget=CheckboxInput(attrs={
                'class': 'seleccion_si_no', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("¿Es una organización comunal?"), 'value': 'S',
            }
        )
    )

    ## Actividad económica principal
    actividad = ChoiceField(
        label=_("Actividad Económica Principal"),
        widget=Select(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Seleccione la Actividad Económica Principal que realiza"),
                'onchange': 'deshabilitar_opcion(this.value,"#id_actividad2")'
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
                'title': _("Código SITUR de la organización comunal"), 'size': '40', 'readonly': 'readonly'
            }
        ), required=False
    )

    ## Casa Matriz de alguna Franquicia
    casa_matriz_franquicia = ChoiceField(
        label=_("¿Es la casa matríz?"),
        choices=((True,''), (False,'')),
        widget=CheckboxInput(attrs={
                'class': 'seleccion_si_no', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("¿Es la casa matríz?"),
                'onchange': "habilitar($(this).is(':checked'), nro_franquicia.id)",
            }
        )
    )

    ## Número de Franquicias asociadas a la Unidad Económica
    nro_franquicia = CharField(
        label=_("Número de Franquicias:"),
        widget=NumberInput(
            attrs={
                'class': 'form-control input-sm', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Número de Franquicias de la Unidad Económica"), 'size': '3', 'min':'1', 'step':'1',
                'readonly': 'readonly',
            }
        ), required=False,
    )

    ## Franquiciado
    franquiciado = ChoiceField(
        label=_("¿Es una Franquicia?"),
        choices=((True,''), (False,'')),
        widget=CheckboxInput(attrs={
                'class': 'seleccion_si_no', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("¿Es una Franquicia?"),
                'onchange': "habilitar($(this).is(':checked'), pais_franquicia.id), habilitar($(this).is(':checked'), nombre_franquicia.id)",
            }
        )
    )

    ## País de la Franquicia
    pais_franquicia = ChoiceField(
        label=_("País de Origen de la Franquicia"),
        widget=Select(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
                'title': _("Seleccione el país de origen de la franquicia"), 'disabled': 'disabled',
                'onchange': """habilitar(this.value, rif_casa_matriz_0.id),
                habilitar(this.value, rif_casa_matriz_1.id), habilitar(this.value, rif_casa_matriz_2.id), deshabilitar(this.value, nombre_franquicia.id, rif_casa_matriz_0.id, rif_casa_matriz_1.id, rif_casa_matriz_2.id)"""
            }
        ), required=False,
    )

    ## Nombre de la Franquicia
    nombre_franquicia = CharField(
        label=_("Nombre de la Franquicia"),
        widget=TextInput(
            attrs={
                'class': 'form-control', 'data-toggle': 'tooltip',
                'title': _("Nombre de la franquicia"), 'size': '40', 'readonly': 'readonly'
            }
        ), required=False
    )

    ## RIF Franquicia
    rif_casa_matriz = RifField(disabled=True, required=False)

    def clean_nro_franquicia(self):
        casa_matriz_franquicia = self.cleaned_data.get('casa_matriz_franquicia')
        nro_franquicia = self.cleaned_data.get('nro_franquicia')

        if(casa_matriz_franquicia=='True' and (nro_franquicia == '' or nro_franquicia == '0')):
            raise forms.ValidationError(_("Indique el número de franquicias"))
        return nro_franquicia
        
    def clean_tipo_comunal(self):
        tipo_comunal = self.cleaned_data['tipo_comunal']
        orga_comunal = self.cleaned_data['orga_comunal']
        if orga_comunal=='True' and not tipo_comunal:
            raise forms.ValidationError(_("Seleccione un tipo de organización comunal"))

        return tipo_comunal

    def clean_situr(self):
        situr = self.cleaned_data['situr']
        orga_comunal = self.cleaned_data['orga_comunal']

        if orga_comunal == 'True' and not situr:
            raise forms.ValidationError(_("Indique el código SITUR de la organización comunal"))
        return situr

    def clean_pais_franquicia(self):
        franquiciado = self.cleaned_data['franquiciado']
        pais_franquicia = self.cleaned_data.get('pais_franquicia', False)

        if franquiciado == 'True' and not pais_franquicia:
            raise forms.ValidationError(_("Indique el país de origen de la franquicia"))
        return pais_franquicia

    def clean_rif_casa_matriz(self):
        rif_casa_matriz = self.cleaned_data['rif_casa_matriz']
        pais_franquicia = self.cleaned_data.get('pais_franquicia')

        if pais_franquicia == '1' and not rif_casa_matriz:
            raise forms.ValidationError(_("Indique el RIF de la franquicia"))
        return rif_casa_matriz

    def clean_nombre_franquicia(self):
        franquiciado = self.cleaned_data['franquiciado']
        pais_franquicia = self.cleaned_data.get('pais_franquicia')
        nombre_franquicia = self.cleaned_data['nombre_franquicia']

        if franquiciado == 'True' and  pais_franquicia == '1' and not nombre_franquicia:
            raise forms.ValidationError(_("Indique nombre de la franquicia"))
        return nombre_franquicia
    
    def clean_rif(self):
        rif = self.cleaned_data['rif']
        if(UnidadEconomica.objects.filter(rif=rif)):
            raise forms.ValidationError(_("Este RIF ya se encuentra registrado"))
        return rif

    def clean(self):
        casa_matriz_franquicia = self.cleaned_data.get('casa_matriz_franquicia')
        franquiciado = self.cleaned_data.get('franquiciado')
        if casa_matriz_franquicia == 'False':
            msg = "Debe tener una Casa Matriz para poder tener Franquicia."
            self.add_error('franquiciado', msg)

    class Meta(object):
        model = UnidadEconomica
        fields = ['rif', 'razon_social', 'nombre_ue']

