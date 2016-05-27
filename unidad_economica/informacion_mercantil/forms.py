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
    ModelForm, TextInput, EmailInput, CharField, EmailField, NumberInput, ChoiceField, Select
)
from django.utils.translation import ugettext_lazy as _
from six import python_2_unicode_compatible
from base.constant import NATURALEZA_JURIDICA, CARGO_REP
from base.fields import RifField, CedulaField
from base.widgets import RifWidgetReadOnly
from base.models import Pais
from unidad_economica.models import UnidadEconomica
from unidad_economica.informacion_mercantil.models import RepresentanteLegal
from django.core import validators

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

@python_2_unicode_compatible
class InformacionMercantilForms(ModelForm):
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
        choices=NATURALEZA_JURIDICA,
        widget=Select(
            attrs={
                'class': 'form-control input-sm', 'size': '28',
                'onchange': "habilitar1(this.value, 'id_naturaleza_juridica_otros')"
            })
    )

    ## Establece el tipo de capital solicitado: capital suscrito
    capital_suscrito = CharField(
        label=_("Capital Social Suscrito: "),
        widget=NumberInput(
            attrs={
                'class': 'form-control input-sm',
                'data-toggle': 'tooltip', 'size': '28',
                'title': _("Indique el Capital Social Suscrito")
            })

    )

    ## Tipo de capital solicitado: capital pagado
    capital_pagado = CharField(
        label=_("Capital Social Pagado: "),
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm',
                'data-toggle': 'tooltip', 'size': '28',
                'title': _("Indique el Capital Social Pagado")
            })
    )

    ## Tipo de capital solicitado: capital publico nacional
    publico_nacional = CharField(
        label=_("Público Nacional: "),
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'size': '2'
            })

    )

    ## Tipo de capital solicitado: capital público extranjero
    publico_extranjero = CharField(
        label=_("Público Extranjero: "), max_length=2,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'size': '2'
            })
    )

    ## Tipo de capital solicitado: capital privado nacional
    privado_nacional = CharField(
        label=_("Privado Nacional: "), max_length=2,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'size': '2'
                })
    )

    ## Tipo de capital solicitado: capital privado
    privado_extranjero = CharField(
        label=_("Privado Extranjero: "), max_length=2,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'size': '2'
            })
    )

    ## Rif del accionista
    rif_accionista = RifField()


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
        choices=[(pais.id, pais.nombre) for pais in Pais.objects.all()]
    )


    ## Porcentaje de acciones que posee el accionista
    porcentaje = CharField(
        label=_("Porcentaje de acciones: "), max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _("Porcentaje"), 'size': '5'
        })
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
    """
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
    """

    ## Cargo que ejerce el representante legal dentro de la unidad económica
    cargo = ChoiceField(
        label=_("Cargo: "),
        choices=CARGO_REP,
        widget=Select(
            attrs={
                'class': 'form-control input-sm', 'size': '28',
                'onchange': "habilitar1(this.value, 'id_cargo_otros')"
            })
    )

    ## Campo para agregar el cargo que ejerce el representante legal en la unidad económica
    cargo_otros = CharField(
        label=_("Otros: "),
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'size': '28', 'disabled': 'disabled'
            }), required=False
    )

    class Meta:
        model = RepresentanteLegal
        fields = [
            'rif_accionista', 'nombre_representante', 'apellido_representante', 'telefono', 'correo_electronico'
            ]
        #exclude = ['naturaleza_juridica_otros']

