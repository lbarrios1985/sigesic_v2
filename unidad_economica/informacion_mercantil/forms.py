from django import forms
from django.forms import (
    ModelForm, TextInput, EmailInput, CharField, EmailField, PasswordInput
)
from django.utils.translation import ugettext_lazy as _
from six import python_2_unicode_compatible
from .models import CapitalAccionista
from base.constant import NATURALEZA_JURIDICA

@python_2_unicode_compatible
class CapitalAccionistaForms(ModelForm):

    natura_jurid = CharField(
        label=_("Naturaleza Jurídica"),
         widget=TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip',
            'title': _("Naturaleza Jurídica"), 'size': '28'
        })
    )

    ## Establece el tipo de capital solicitado: capital suscrito
    capital_suscrito = CharField(
        label=_("Capital Social Suscrito: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("Indique el Capital Social Suscrito"), 'data-toggle': 'tooltip',
            'title': _("Capital Social Suscrito"), 'size': '28'
        })
    )
    ## Establece el tipo de capital solicitado: capital pagado
    capital_pagado = CharField(
        label=_("Capital Social Pagado: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("Indique el Capital Pagado"), 'data-toggle': 'tooltip',
            'title': _("Capital Pagado"), 'size': '28'
        })
    )
    ## Establece el tipo de capital solicitado: capital privado
    capital_privado = CharField(
        label=_("Capital Privado: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip',
            'title': _("Capital Privado"), 'size': '2'
        })
    )
    ## Establece el tipo de capital solicitado: capital publico
    capital_publico = CharField(
        label=_("Capital Público: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("Indique el Capital Público"), 'data-toggle': 'tooltip',
            'title': _("Capital Público"), 'size': '28'
        })
    )
    ## Establece el tipo de capital solicitado: capital nacional
    capital_nacional = CharField(
        label=_("Capital Nacional: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("Indique el Capital Nacional"), 'data-toggle': 'tooltip',
            'title': _("Capital Nacional"), 'size': '28'
        })
    )
    ## Establece el tipo de capital solicitado: capital extranjero
    capital_externo = CharField(
        label=_("Capital Extranjero: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("Indique el Capital Extranjero"), 'data-toggle': 'tooltip',
            'title': _("Capital Extranjero"), 'size': '28'
        })
    )
    ##Establece el tipo de persona
    tipo_persona_id = CharField(
        label=_("Tipo de Persona: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("Indique el Tipo de Persona"), 'data-toggle': 'tooltip',
            'title': _("Tipo de persona"), 'size': '28'
        })
    )
    ##Establece el rif del accionista
    rif_accionista = CharField(
        label=_("RIF: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("Indique el RIF"), 'data-toggle': 'tooltip',
            'title': _("RIF del Accionista"), 'size': '28'
        })
    )
    ##Establece el nombre del accionista
    nombre = CharField(
        label=_("Nombre SENIAT: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("Nombre SENIAT"), 'data-toggle': 'tooltip',
            'title': _("Nombre SENIAT"), 'size': '28'
        })
    )
    ##Establece el porcentaje de acciones que posee el accionista
    porcentaje = CharField(
        label=_("Porcentaje de acciones: "), max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip',
            'title': _("Porcentaje"), 'size': '15'
        })
    )

    class Meta:
        model = CapitalAccionista
        exclude = ['porcentaje',]
