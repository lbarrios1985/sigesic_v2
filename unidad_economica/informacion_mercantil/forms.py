from __future__ import unicode_literals, absolute_import
from django.forms import (
    ModelForm, TextInput, EmailInput, CharField, EmailField, NumberInput
)
from django.utils.translation import ugettext_lazy as _
from six import python_2_unicode_compatible
from .models import CapitalAccionista
from base.constant import NATURALEZA_JURIDICA, TIPO_PERSONA_LIST
from base.fields import RifField, CedulaField
from base.forms import RifForm
from base.widgets import RifWidgetReadOnly


@python_2_unicode_compatible
class CapitalAccionistaForms(ModelForm):

    ## Naturaleza Jurídica
    naturaleza_juridica = NATURALEZA_JURIDICA

    ## Establece el tipo de capital solicitado: capital suscrito
    capital_suscrito = CharField(
        label=_("Capital Social Suscrito: "), max_length=30,
        widget=NumberInput(attrs={
            'class': 'form-control input-sm', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
            'title': _("Indique el Capital Social Pagado"), 'size': '28',
        }), required=True
    )

    ## Tipo de capital solicitado: capital pagado
    capital_pagado = CharField(
        label=_("Capital Social Pagado: "), max_length=30,
        widget=NumberInput(attrs={
            'class': 'form-control input-sm', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
            'title': _("Indique el Capital Social Pagado"), 'size': '28',
        }), required=True
    )

    ## Tipo de capital solicitado: capital publico nacional
    publico_nacional = CharField(
        label=_("Capital Público Nacional: "), max_length=30,
        widget=NumberInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'size': '28'
        }), required=True
    )

    ## Tipo de capital solicitado: capital público extranjero
    publico_extranjero = CharField(
        label=_("Capital Público Extranjero: "), max_length=2,
        widget=NumberInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'size': '28'
        }), required=True
    )

    ## Tipo de capital solicitado: capital privado nacional
    privado_nacional = CharField(
        label=_("Capital Privado Nacional: "), max_length=2,
        widget=NumberInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip',
            'title': _("Capital Privado"), 'size': '2'
        }), required=True
    )

    ## Tipo de capital solicitado: capital privado
    privado_extranjero = CharField(
        label=_("Capital Privado Extranjero: "), max_length=30,
        widget=NumberInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip',
        }), required=True
    )

    ## Tipo de persona
    tipo_persona_id = CharField(
        label=_("Tipo de Persona: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("Indique el Tipo de Persona"), 'data-toggle': 'tooltip',
            'title': _("Tipo de persona"), 'size': '28'
        }), required=True
    )

    ## Rif del accionista
    rif_accionista = RifField()
    ##rif_accionista = RifWidgetReadOnly

    ## Nombre del accionista
    nombre_accionista = CharField(
        label=_("Nombre SENIAT: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("Nombre SENIAT"), 'data-toggle': 'tooltip',
            'title': _("Nombre SENIAT"), 'size': '28'
        }), required=True
    )

    ## Porcentaje de acciones que posee el accionista
    porc_acciones = CharField(
        label=_("Porcentaje de acciones: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip',
            'title': _("Porcentaje"), 'size': '15'
        }), required=True
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


    class Meta:
        model = CapitalAccionista
        fields = [
            'rif_rep', 'cedula_rep', 'cargo_rep', 'nombre_rep', 'apellido_rep', 'telefono_rep', 'correo_rep'
            ]

    def clean_rif(self):
        """!
        Método que permite validar el campo de rif

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 27-04-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que el rif no sea válido o no se encuentre registrado en el
                SENIAT, en caso contrario devuelve el valor actual del campo
        """
        rif = self.cleaned_data['rif']

        if rif[0] not in TIPO_PERSONA_LIST:
            raise forms.ValidationError(_("Tipo de RIF incorrecto"))
        elif User.objects.filter(username=rif):
            raise forms.ValidationError(_("El RIF ya se encuentra registrado"))
        elif not rif[1:].isdigit():
            raise forms.ValidationError(_("El RIF no es correcto"))

        return rif

