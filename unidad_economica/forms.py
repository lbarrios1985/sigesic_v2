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
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Nombre Comercial de la Unidad Económica a registrar"), 'size': '50', 'disabled': 'disabled'
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
        ), required=False
    )

    ## Actividad económica principal
    actividad = ChoiceField(
        label=_("Actividad Económica Principal"),
        choices=[(actividad.codigo_ciiu, actividad.descripcion) for actividad in Ciiu.objects.all()]
    )

    ## Número de Plantas Productivas de la Unidad Económica
    nro_planta = CharField(
        label=_("Número de Plantas Productivas:"),
        widget=TextInput(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Número de Plantas Productivas de la Unidad Económica"), 'size': '1', 'maxlength': '2'
            }
        )
    )

    ## Número de Unidades Comercializadoras 
    nro_unid_comercializadora = CharField(
        label=_("Número de Unidades Comercializadoras:"),
        widget=TextInput(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Número de Unidades Comercializadoras de la Unidad Económica"), 'size': '1'
            }
        )
    )

    ## Servicios que presta la Unidad Económica
    servicio = ChoiceField(
        label=_("¿Presta algún servicio?"),
        choices=SELECCION
    )

    ## Organización comunal
    orga_comunal = ChoiceField(
        label=_("¿Es una organización comunal?"),
        choices=SELECCION,
        widget=Select(attrs={
                'onchange': "habilitar(this.value, tipo_comunal.id), habilitar(this.value, situr.id)",
            }
        )
    )

    ## Tipo de organización comunal
    tipo_comunal = ChoiceField(
        label=_("Tipo de Organizacón Comunal: "),
        choices=[(comunal.id, comunal.tipo_comunal) for comunal in TipoComunal.objects.all()],
        widget=Select(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Seleccione el tipo de Organizacón Comunal"), 'disabled': 'disabled'
            }
        )
    )

    ## Código SITUR
    situr = CharField(
        label=_("Código SITUR:"),
        widget=TextInput(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Código SITUR de la organización comunal"), 'size': '40', 'disabled': 'disabled'
            }
        )
    )

    ## Casa Matriz de alguna Franquicia
    casa_matriz_franquicia = ChoiceField(
        label=_("¿Es la casa matríz de una Franquicia?"),
        choices=SELECCION,
        widget=Select(attrs={
                'onchange': "habilitar(this.value, nro_franquicia.id)",
            }
        )
    )

    ## Número de Franquicias asociadas a la Unidad Económica
    nro_franquicia = CharField(
        label=_("Número de Franquicias:"),
        widget=TextInput(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Número de Franquicias de la Unidad Económica"), 'size': '1', 'disabled': 'disabled' 
            }
        )
    )

    ## Franquiciado
    franquiciado = ChoiceField(
        label=_("¿Forma parte de una Franquicia?"),
        choices=SELECCION,
        widget=Select(attrs={
                'onchange': "habilitar(this.value, pais_franquicia.id), habilitar(this.value, nombre_franquicia.id)",
            }
        )
    )

    ## País de la Franquicia
    pais_franquicia = ChoiceField(
        label=_("País de Origen de la Franquicia"),
        choices=[(pais.id, pais.nombre) for pais in Pais.objects.all()],
        widget=Select(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Seleccione el país de origen de la franquicia"), 'disabled': 'disabled'
            }
        )
    )

    ## Nombre de la Franquicia
    nombre_franquicia = CharField(
        label=_("Nombre de la Franquicia"),
        widget=TextInput(
            attrs={
                'class': 'form-control', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Nombre de la franquicia"), 'size': '40', 'disabled': 'disabled'
            }
        )
    )

    ## RIF Franquicia
    rif_franquicia = RifField()
    rif_franquicia.widget = RifWidgetReadOnly()