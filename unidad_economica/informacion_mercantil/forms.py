"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
##  @package informacion_mercantil.forms
#
# Formulario para las distintas clases de la informacion mercantil de la unidad económica
# @author Lully Troconis (ltroconis at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 04-05-2016
# @version 2.0from __future__ import unicode_literals, absolute_import

from __future__ import unicode_literals
from django.forms import (
    ModelForm, TextInput, EmailInput, CharField, EmailField, NumberInput, ChoiceField, Select, DecimalField
)
from django.utils.translation import ugettext_lazy as _
from six import python_2_unicode_compatible
from base.constant import NATURALEZA_JURIDICA, CARGO_REP
from base.fields import RifField, CedulaField
from base.models import Pais
from base.functions import cargar_pais
from unidad_economica.informacion_mercantil.models import RepresentanteLegal
from django.core import validators
from django.core.exceptions import ValidationError

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

@python_2_unicode_compatible
class InformacionMercantilForm(ModelForm):
    """!
    Formulario para la gestión de la información mercantil: capital, accionistas y representante legal.

    @author Lully Troconis (ltroconis at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 04-05-2016
    @version 2.0
    """

    ## Naturaleza Jurídica
    naturaleza_juridica = ChoiceField(
        label=_("Naturaleza Jurídica: "),
        choices=[('', 'Seleccione...')]+NATURALEZA_JURIDICA,
        widget=Select(
            attrs={
                'class': 'form-control input-sm', 'size': '28',
            }
        )
    )

    ## Establece el tipo de capital solicitado: capital suscrito
    capital_suscrito = CharField(
        label=_("Capital Social Suscrito: "),max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm porcentaje', 'data-toggle': 'tooltip', 'size': '28'
        })
    )

    ## Tipo de capital solicitado: capital pagado
    capital_pagado = CharField(
        label=_("Capital Social Pagado: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm porcentaje', 'data-toggle': 'tooltip', 'size': '28',
        })
    )

    ## Tipo de capital solicitado: capital publico nacional
    publico_nacional = CharField(
        label=_("Público Nacional: "), max_length=6,
        widget=TextInput(attrs={
            'class': 'form-control input-sm porcentaje', 'data-toggle': 'tooltip', 'size': '4',
        })
    )

    ## Tipo de capital solicitado: capital público extranjero
    publico_extranjero = CharField(
        label=_("Público Extranjero: "), max_length=6,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm porcentaje', 'data-toggle': 'tooltip', 'size': '4',
            }
        )
    )

    ## Tipo de capital solicitado: capital privado nacional
    privado_nacional = CharField(
        label=_("Privado Nacional: "), max_length=6,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm porcentaje', 'data-toggle': 'tooltip', 'size': '4'
            }
        )
    )

    ## Tipo de capital solicitado: capital privado
    privado_extranjero = CharField(
        label=_("Privado Extranjero: "), max_length=6,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm porcentaje', 'data-toggle': 'tooltip', 'size': '4'
            }
        )
    )

    ## Rif del accionista
    rif_accionista_orig = RifField(required=False)

    ## Nombre del accionista
    nombre = CharField(
        label=_("Nombre: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("Nombre"), 'data-toggle': 'tooltip',
            'title': _("Nombre "), 'size': '28', 'readonly': 'readonly'
        }), required=False
    )

    # País de origen del accionista
    pais_origen = ChoiceField(
        label=_("País de origen: "),
        required=False
    )


    ## Porcentaje de acciones que posee el accionista
    porcentaje = CharField(
        label=_("Porcentaje de acciones: "), max_length=3,
        widget=NumberInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _("Porcentaje"), 'size': '5'
            }
        ), required=False
    )

    ## Campo oculto para el RIF del accionista
    rif_accionista_tb = CharField(
        label=_("Ingrese el R.I.F del accionista"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: 0; width: auto; display: inline;', 'value': 'rif',
            'size': '30',
        }),
    )

    ## Campo oculto para el nombre del accionista
    nombre_tb = CharField(
        widget=TextInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: 0; width: auto; display: inline;', 'size': '30',
        }),
    )

    ## Campo oculto para el país de origen del accionista
    pais_origen_tb = CharField(
        label=_("Seleccione el país del accionista"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: 0; width: auto; display: inline;', 'size': '30',
        }),required=False,
    )

    ## Campo oculto para el porcentaje de acciones que posee el accionista
    porcentaje_tb = CharField(
        label=_("Seleccione el país del accionista"), widget=TextInput(attrs={
            'class': 'form-control input-md', 'style': 'min-width: 0; width: auto; display: inline;', 'size': '30',
        }),
    )

    ## Cédula de identidad del representante legal
    cedula_representante = CedulaField()

    ## Nombre del Representante Legal
    nombre_representante = CharField(
        label=_("Nombre: "),
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Nombres del usuario"), 'data-rule-required': 'true',
                'data-toggle': 'tooltip', 'title': _("Indique el Nombre"), 'size': '50'
            }
        )
    )

    ## Apellido del representante legal
    apellido_representante = CharField(
        label=_("Apellido: "),
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Apellidos del usuario"), 'data-rule-required': 'true',
                'data-toggle': 'tooltip', 'title': _("Indique el Apellido"), 'size': '50'
            }
        )
    )

    ## Correo electrónico del representante legal
    correo_electronico = EmailField(
        label=_("Correo Electrónico: "),
        max_length=75,
        widget=EmailInput(
            attrs={
                'class': 'form-control input-sm email-mask', 'placeholder': _("Correo de contacto"),
                'data-toggle': 'tooltip', 'size': '50', 'data-rule-required': 'true',
                'title': _("Indique el correo electrónico de contacto con el usuario. "
                           "No se permiten correos de hotmail")
            }
        )
    )

    ## Número telefónico del representante legal
    telefono = CharField(
        label=_("Teléfono: "),
        max_length=20,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': '(058)-000-0000000',
                'data-rule-required': 'true', 'data-toggle': 'tooltip', 'size': '15',
                'title': _("Indique el número telefónico de contacto con el usuario"), 'data-mask': '(000)-000-0000000'
            }
        ),
        help_text=_("(país)-área-número")
    )


    ## Cargo que ejerce el representante legal dentro de la unidad económica
    cargo = ChoiceField(
        label=_("Cargo: "),
        choices=[('', 'Seleccione...')]+CARGO_REP,
        widget=Select(
            attrs={
                'class': 'form-control input-sm', 'size': '28',
                'onchange': "habilitar(this.value, 'id_cargo_otros')"
            }
        )
    )

    ## Campo para agregar el cargo que ejerce el representante legal en la unidad económica
    cargo_otros = CharField(
        label=_("Otros: "),
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'size': '28', 'disabled': 'disabled'
            }
        ), required=False
    )

    rif_ue = RifField(required=False)

    def __init__(self, *args, **kwargs):
        super(InformacionMercantilForm, self).__init__(*args, **kwargs)

        self.fields['pais_origen'].choices = cargar_pais()

    class Meta:
        model = RepresentanteLegal
        fields = ['cargo_otros']
