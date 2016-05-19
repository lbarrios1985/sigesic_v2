from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from unidad_economica.models import UnidadEconomica


@python_2_unicode_compatible
class Capital(models.Model):
    """!
    Clase que gestiona el capital de la información mercantil en el sistema

    @author Lully Troconis
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 03-05-2016
    @version 2.0.0
    """

    ## Establece el rif de la unidad economica
    rif_ue = models.ForeignKey(UnidadEconomica)


    ##Establece el capital solicitado: capital suscrito
    capital_suscrito = models.FloatField(
        max_length=2, help_text=_("Capital Suscrito"),
        validators=[
            validators.RegexValidator(
                r'^[\d.,]+$',
                _("Sólo se permiten números.")
            ),
        ]
    )

    ## Establece el tipo de capital solicitado: capital pagado
    capital_pagado = models.FloatField(
        max_length=2,
        help_text=("Capital Pagado")
    )

    ## Establece el tipo de capital solicitado: capital privado
    capital_privado = models.FloatField(
        max_length=2, help_text=_("Capital Privado"),
        validators=[
            validators.RegexValidator(
                r'^[\d.,]+$',
                _("Sólo se permiten números.")
            ),
        ]
    )

    ## Establece el tipo de capital solicitado: capital publico nacional
    capital_publico = models.FloatField(
        max_length=2, help_text=_("Capital Público"),
        validators=[
            validators.RegexValidator(
                r'^[\d.,]+$',
                _("Sólo se permiten números.")
            ),
        ]
    )

    ## Establece el tipo de capital solicitado: capital externo
    capital_externo = models.FloatField(
        max_length=2, help_text=_("Capital Público"),
        validators=[
            validators.RegexValidator(
                r'^[\d.,]+$',
                _("Sólo se permiten números.")
            ),
        ]
    )

class Accionista(models.Model):

    """!
    Clase que gestiona el capital de la información mercantil en el sistema

    @author Lully Troconis
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 03-05-2016
    @version 2.0.0
    """

    rif_ue = models.ForeignKey(UnidadEconomica)

    ## Establece el rif del accionista
    rif_accionista = models.CharField(
        max_length=10
    )

    ## Establece el nombre del accionista
    nombre = models.CharField(
        max_length=45, help_text=_("Nombre del Accionista")
    )

    ## Establece el porcentaje de acciones que posee el accionista
    porcentaje = models.FloatField(
        help_text=_("Porcentaje de accciones que posee el acionista")
    )

class RepresentanteLegal(models.Model):


    rif_ue = models.ForeignKey(UnidadEconomica)


    ## Establece la Cédula de Identidad del Representante Legal
    cedula_representante = models.CharField(
        max_length=8, help_text=_("Cédula de Identidad del usuario"),
        validators=[
            validators.RegexValidator(
                r'^[\d]{7,8}+$',
                _("Introduzca un número de cédula válido. Solo se permiten números y una longitud de 7 u 8 carácteres.")
            ),
        ]
    )


    ## Establece el nombre del Representante Legal
    nombre_representante = models.CharField(
        max_length=45, help_text=("Nombre del Representante Legal")
    )

    ## Establece el apellido del Representante Legal
    apellido_representante = models.CharField(
        max_length=45, help_text=("Apellido del Representante Legal")
    )

    ## Establece el correo electrónico del Represntante Legal
    correo_electronico = models.CharField(
        max_length=45, help_text=("correo@dssddsd.com")
    )

    ## Establece el número telefónico del Representante Legal
    telefono = models.CharField(
        max_length=20, help_text=_("Número telefónico de contacto con el usuario"),
        validators=[
            validators.RegexValidator(
                r'^[\d+-]+$',
                _("Número telefónico inválido. Solo se permiten números, y los signos + o -")
            ),
        ]
    )

    ##Establece el cargo del Representante Legal
    cargo = models.CharField(max_length=1)


