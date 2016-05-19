from __future__ import unicode_literals, absolute_import
from django.forms import (
    ModelForm, TextInput, EmailInput, CharField, EmailField, NumberInput, ChoiceField, Select
)
from django.utils.translation import ugettext_lazy as _
from six import python_2_unicode_compatible
from .models import CapitalAccionista
from base.constant import NATURALEZA_JURIDICA, CARGO_REP
from base.fields import RifField, CedulaField
from base.widgets import RifWidgetReadOnly
from base.models import Pais

@python_2_unicode_compatible
class CapitalAccionistaForms(ModelForm):

    ## Naturaleza Jurídica
    naturaleza_juridica = ChoiceField(
        label=_("Naturaleza Jurídica: "),
        choices=NATURALEZA_JURIDICA,
        widget=Select(
            attrs={
         'class': 'form-control input-sm', 'size': '28',
        # 'onchange': "habilitar(naturaleza_juridica, naturaleza_juridica_otros)"
        })
    )
    naturaleza_juridica_otros = CharField(
        label=_("Otros: "),
        widget=TextInput(
            attrs={
            'class': 'form-control input-sm', 'size': '28',
            #'style': 'display: none',
            #'disabled': 'true',
            'onchange': "habilitar(this.value, '0', 'naturaleza_juridica_otros')"
        })
    )

    ## Establece el tipo de capital solicitado: capital suscrito
    capital_suscrito = CharField(
        label=_("Capital Social Suscrito: "),
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'size': '2'
        })
    )

    ## Tipo de capital solicitado: capital pagado
    capital_pagado = CharField(
        label=_("Capital Social Pagado: "),
        widget=TextInput(attrs={
            'class': 'form-control input-sm',
            'data-toggle': 'tooltip', 'size': '2', 'data-rule-required': 'true',
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
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'size': '2'
        })
    )

    ## Tipo de capital solicitado: capital privado nacional
    privado_nacional = CharField(
        label=_("Privado Nacional: "), max_length=2,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'size': '2'
        })
    )

    ## Tipo de capital solicitado: capital privado
    privado_extranjero = CharField(
        label=_("Privado Extranjero: "), max_length=2,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'size': '2'
        })
    )

    ## Rif del accionista
    rif_accionista = RifField()
    #rif_accionista.widget = RifWidgetReadOnly()

    ## Nombre del accionista
    nombre_accionista = CharField(
        label=_("Nombre SENIAT: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("Nombre SENIAT"), 'data-toggle': 'tooltip',
            'title': _("Nombre SENIAT"), 'size': '28'
        }), required=True
    )

    pais_origen = ChoiceField(
        label=_("País de origen: "),
        choices=[(pais.id, pais.nombre) for pais in Pais.objects.all()]
    )

    ## Porcentaje de acciones que posee el accionista
    porc_acciones = CharField(
        label=_("Porcentaje de acciones: "), max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _("Porcentaje"), 'size': '5'
        })
    )

    ## Cédula de identidad del Representante Legal
    cedula_rep = CedulaField()

    nombre_rep = CharField(
        label=_("Nombre"),
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Nombres del usuario"), 'data-rule-required': 'true',
                'data-toggle': 'tooltip', 'title': _("Indique el Nombre"), 'size': '50'
            }
        )
    )

    ## Apellido del Representante Legal
    apellido_rep = CharField(
        label=_("Apellido"),
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Apellidos del usuario"), 'data-rule-required': 'true',
                'data-toggle': 'tooltip', 'title': _("Indique el Apellido"), 'size': '50'
            }
        )
    )

    ## Correo electrónico de contacto del Representante Legal
    correo_rep = EmailField(
        label=_("Correo Electrónico"),
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

    ## Número telefónico de contacto del Representante Legal
    telefono_rep = CharField(
        label=_("Teléfono"),
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

    ## Cargo que ejerce el Representante Legal
    cargo_rep = ChoiceField(
        label=_("Cargo: "),
        choices=CARGO_REP
    )


    class Meta:
        model = CapitalAccionista
        fields = [
            'rif_rep', 'cedula_rep', 'cargo_rep', 'nombre_rep', 'apellido_rep', 'telefono_rep', 'correo_rep'
            ]
        exclude = ['naturaleza_juridica_otros']

