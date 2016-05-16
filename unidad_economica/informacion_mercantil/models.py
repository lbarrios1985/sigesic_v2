from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from base.constant import NATURALEZA_JURIDICA


@python_2_unicode_compatible
class CapitalAccionista(models.Model):
    """!
    Clase que gestiona el capital de la información mercantil en el sistema

    @author Lully Troconis
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 03-05-2016
    @version 2.0.0
    """

    ## Establece la nacionalidad del usuario
    naturaleza_juridica = models.CharField(
        max_length=1, choices=NATURALEZA_JURIDICA,
    )


    ##Establece el capital solicitado: capital suscrito
    capital_suscrito = models.CharField(
        max_length=15, help_text=_("Capital Suscrito"),
        validators=[
            validators.RegexValidator(
                r'^[\d.,]+$',
                _("Sólo se permiten números.")
            ),
        ]
    )

    ## Establece el tipo de capital solicitado: capital pagado
    capital_pagado = models.FloatField(
        help_text=("Capital Pagado")
    )

    ## Establece el tipo de capital solicitado: capital privado
    capital_privado = models.FloatField(
        max_length=15, help_text=_("Capital Privado"),
        validators=[
            validators.RegexValidator(
                r'^[\d.,]+$',
                _("Sólo se permiten números.")
            ),
        ]
    )

    ## Establece el tipo de capital solicitado: capital publico nacional
    capital_publico = models.FloatField(
        max_length=15, help_text=_("Capital Público"),
        validators=[
            validators.RegexValidator(
                r'^[\d.,]+$',
                _("Sólo se permiten números.")
            ),
        ]
    )

    ## Establece el tipo de capital solicitado: capital externo
    capital_externo = models.FloatField(
        max_length=15, help_text=_("Capital Público"),
        validators=[
            validators.RegexValidator(
                r'^[\d.,]+$',
                _("Sólo se permiten números.")
            ),
        ]
    )

    ## Establece el tipo de persona
    tipo_persona_id = models.CharField(
        max_length=10, help_text=_("ID persona")
    )

    ## Establece el rif del accionista
    rif_accionista = models.CharField(max_length=10)

    ## Establece el nombre del accionista
    nombre_accionista = models.CharField(
        max_length=15, help_text=_("Nombre del Accionista")
    )

    ## Establece el porcentaje de acciones que posee el accionista
    porc_acciones = models.CharField(
        max_length=2, help_text=_("Porcentaje de accciones que posee el acionista")
    )

    ## Establece la Cédula de Identidad del Representante Legal
    cedula_rep = models.CharField(
        max_length=8, help_text=_("Cédula de Identidad del usuario"),
        validators=[
            validators.RegexValidator(
                r'^[\d]{7,8}+$',
                _("Introduzca un número de cédula válido. Solo se permiten números y una longitud de 7 u 8 carácteres.")
            ),
        ]
    )

    rif_rep = models.CharField(max_length=8)

    ## Establece el nombre del Representante Legal
    nombre_rep = models.CharField(
        max_length=15, help_text=("Nombre del Representante Legal")
    )

    ## Establece el apellido del Representante Legal
    apellido_rep = models.CharField(
        max_length=15, help_text=("Apellido del Representante Legal")
    )

    ## Establece el correo electrónico del Represntante Legal
    correo_rep = models.CharField(
        max_length=15, help_text=("correo@dssddsd.com")
    )

    ## Establece el número telefónico del Representante Legal
    telefono_rep = models.CharField(
        max_length=20, help_text=_("Número telefónico de contacto con el usuario"),
        validators=[
            validators.RegexValidator(
                r'^[\d+-]+$',
                _("Número telefónico inválido. Solo se permiten números, y los signos + o -")
            ),
        ]
    )

    ##Establece el correo electrónico del Represntante Legal
    cargo_rep = models.CharField(
        max_length=175, help_text=_("Cargo del usuario dentro de la Unidad Económica")
    )

    class Meta:
        verbose_name = _("Accionista")
        verbose_name_plural = _("Accionistas")
        # ordering = ("",)
