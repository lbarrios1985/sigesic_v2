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
from django import forms
from django.forms import (
    ModelForm, TextInput, EmailInput, CharField, EmailField, NumberInput, ChoiceField, Select, DecimalField
)
from django.utils.translation import ugettext_lazy as _
from six import python_2_unicode_compatible
from base.constant import NATURALEZA_JURIDICA, CARGO_REP
from base.fields import RifField, CedulaField
from base.models import Pais
from base.functions import cargar_pais
from .models import Capital, RepresentanteLegal
from django.core import validators
from django.core.exceptions import ValidationError
from base.widgets import RifWidgetReadOnly, RifWidget
import re

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

    ## R.I.F. de la Unidad Económica que identifica al usuario en el sistema
    rif = RifField()
    rif.widget = RifWidgetReadOnly()

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
            'class': 'form-control input-sm porcentaje', 'data-toggle': 'tooltip', 'size': '28', 'required':'required',
        })
    )

    ## Tipo de capital solicitado: capital pagado
    capital_pagado = CharField(
        label=_("Capital Social Pagado: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm porcentaje', 'data-toggle': 'tooltip', 'size': '28', 'required':'required',
        })
    )

    ## Tipo de capital solicitado: capital publico nacional
    publico_nacional = CharField(
        label=_("Público Nacional: "), max_length=6,
        widget=TextInput(attrs={
            'class': 'form-control input-sm porcentaje', 'data-toggle': 'tooltip', 'size': '4', 'placeholder': '0', 'required':'required',
            'value': '0',
        })
    )

    ## Tipo de capital solicitado: capital público extranjero
    publico_extranjero = CharField(
        label=_("Público Extranjero: "), max_length=10,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm porcentaje', 'data-toggle': 'tooltip', 'size': '4', 'placeholder': '0', 'required':'required',
                'value': '0',
            }
        )
    )

    ## Tipo de capital solicitado: capital privado nacional
    privado_nacional = CharField(
        label=_("Privado Nacional: "), max_length=6,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm porcentaje', 'data-toggle': 'tooltip', 'size': '4', 'placeholder': '0', 'required':'required',
                'value': '0',
            }
        )
    )

    ## Tipo de capital solicitado: capital privado
    privado_extranjero = CharField(
        label=_("Privado Extranjero: "), max_length=6,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm porcentaje', 'data-toggle': 'tooltip', 'size': '4', 'placeholder': '0', 'required':'required',
                'value': '0',
            }
        )
    )

    ## Rif del accionista
    rif_accionista_orig = RifField(required=False)

    ## Nombre del accionista
    razon_social_accionista = CharField(
        label=_("Razón Social: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip',
            'title': _("Razón Social "), 'size': '28', 'readonly': 'readonly'
        }), required=False
    )

    # País de origen del accionista
    pais_origen = ChoiceField(
        label=_("País de origen: "),
        required=False
    )


    ## Porcentaje de acciones que posee el accionista
    porcentaje = CharField(
        label=_("Porcentaje de acciones: "), max_length=5,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _("Porcentaje"), 'size': '5', 'placeholder': '0',
            }
        ), required=False
    )

    ## campo oculto para verificar que el porcentaje sea 100
    porcentaje_total= CharField(
        widget=TextInput(
            attrs={
                'type':'hidden',
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
    razon_social_accionista_tb = CharField(
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

    ## Rif del representante legal
    rif_representante = RifField()

    ## razón social del Representante Legal
    razon_social_representante = CharField(
        label=_("Razón Social: "),
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-rule-required': 'true',
                'data-toggle': 'tooltip', 'title': _("Razón Social"), 'size': '50', 'readonly':'readonly'
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
                'onchange': "habilitar_cargo(this.value, 'id_cargo_otros')"
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
        user = kwargs.pop('user')
        super(InformacionMercantilForm, self).__init__(*args, **kwargs)

        self.fields['pais_origen'].choices = cargar_pais()

    def clean(self):
        cleaned_data = super(InformacionMercantilForm, self).clean()
        capital_suscrito= self.cleaned_data['capital_suscrito']
        capital_pagado= self.cleaned_data['capital_pagado']
        publico_nacional= self.cleaned_data['publico_nacional']
        publico_extranjero= self.cleaned_data['publico_extranjero']
        privado_nacional= self.cleaned_data['privado_nacional']
        privado_extranjero= self.cleaned_data['privado_extranjero']
        cargo= self.cleaned_data['cargo']
        porcentaje_total= self.cleaned_data['porcentaje_total']

        ## Se se comprueban los datos por expresiones regulares para saber que son números correctos
        ## Luego se convierten a números decimales
        capital_suscrito = capital_suscrito.replace('.', '')
        capital_suscrito = capital_suscrito.replace(',', '.')

        capital_pagado = capital_pagado.replace('.', '')
        capital_pagado = capital_pagado.replace(',', '.')

        result1 = re.match(r"""^[0-9]+(\.[0-9]{1,2})?$""", capital_suscrito)
        result2 = re.match(r"""^[0-9]+(\.[0-9]{1,2})?$""", capital_pagado)

        band= True
        if result1:
            capital_suscrito = float(result1.group(0))
            self.cleaned_data['capital_suscrito']= capital_suscrito
        else:
            band= False
            msg = "Capital Suscrito tiene datos incorrectos."
            self.add_error('capital_suscrito', msg)

        if result2:
            capital_pagado = float(result2.group(0))
            self.cleaned_data['capital_pagado']= capital_pagado
        else:
            band= False
            msg = "Capital Pagado tiene datos incorrectos."
            self.add_error('capital_pagado', msg)

        if band:
            if capital_suscrito < capital_pagado:
                msg = "Capital Suscrito debe ser mayor o igual a Capital Pagado."
                self.add_error('capital_suscrito', msg)

        publico_nacional = publico_nacional.replace(',', '.')
        publico_extranjero= publico_extranjero.replace(',', '.')
        privado_nacional= privado_nacional.replace(',', '.')
        privado_extranjero= privado_extranjero.replace(',', '.')

        result3 = re.match(r"""^[0-9]+(\.[0-9]{1,2})?$""", publico_nacional)
        result4 = re.match(r"""^[0-9]+(\.[0-9]{1,2})?$""", publico_extranjero)
        result5 = re.match(r"""^[0-9]+(\.[0-9]{1,2})?$""", privado_nacional)
        result6 = re.match(r"""^[0-9]+(\.[0-9]{1,2})?$""", privado_extranjero)

        band= True
        if result3:
            publico_nacional = float(result3.group(0))
            self.cleaned_data['publico_nacional']= publico_nacional
        else:
            band= False
            msg = "Público Nacional tiene datos incorrectos."
            self.add_error('publico_nacional', msg)

        if result4:
            publico_extranjero = float(result4.group(0))
            self.cleaned_data['publico_extranjero']= publico_extranjero
        else:
            band= False
            msg = "Público Extranjero tiene datos incorrectos."
            self.add_error('publico_extranjero', msg)

        if result5:
            privado_nacional = float(result5.group(0))
            self.cleaned_data['privado_nacional']= privado_nacional
        else:
            band= False
            msg = "Privado Nacional tiene datos incorrectos."
            self.add_error('privado_nacional', msg)

        if result6:
            privado_extranjero = float(result6.group(0))
            self.cleaned_data['privado_extranjero']= privado_extranjero
        else:
            band= False
            msg = "Privado Extranjero tiene datos incorrectos."
            self.add_error('privado_extranjero', msg)

        if band:
            if (publico_nacional+publico_extranjero+privado_nacional+privado_extranjero) < 100:
                msg = "La suma de todos los elementos de la distribución porcentual del capital suscrito debe ser de 100,00%, por favor verifique...."
                self.add_error('publico_nacional', msg)
            elif (publico_nacional+publico_extranjero+privado_nacional+privado_extranjero) > 100:
                msg = "El porcentaje máximo debe ser 100,00%"
                self.add_error('publico_nacional', msg)

        if cargo != "Otro":
            self.cleaned_data['cargo_otros']= None

        ## Comprueba que el valor del porcentaje total de los accionistas sea correcto
        result7 = re.match(r"""^[0-9]+(\.[0-9]{1,2})?$""", porcentaje_total)
        if result7:
            if float(porcentaje_total) != 100 :
                msg= "El total del Porcentaje de los Accionistas debe ser 100%, verifique..."
                self.add_error('porcentaje', msg)
        else:
            msg= "Porcentaje tiene datos incorrectos."
            self.add_error('porcentaje', msg)

    def clean_rif(self):
        rif= self.cleaned_data['rif']
        if Capital.objects.filter(unidad_economica__rif=rif) and RepresentanteLegal.objects.filter(unidad_economica__rif=rif) :
            raise forms.ValidationError(_("Los datos ya se encuentran registrados"))
        return rif

    class Meta:
        model = Capital
        fields = ['cargo_otros']
