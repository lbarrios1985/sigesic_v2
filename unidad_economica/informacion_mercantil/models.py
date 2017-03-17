"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
##  @package informacion_mercantil.models
#
# Contiene las clases, atributos y métodos para el ítem de Información Mercantil
# @author Lully Troconis (ltroconis at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>

from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from unidad_economica.models import UnidadEconomica
from base.models import Pais

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

@python_2_unicode_compatible
class Capital(models.Model):
    """!
    Clase que gestiona el capital de la información mercantil en el sistema

    @author Lully Troconis (ltroconis at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 03-05-2016
    @version 2.0.0
    """

    ## Establece la naturaleza jurídica de la Unidad Económica
    naturaleza_juridica = models.CharField(max_length=45)

    ##Establece el capital solicitado: capital suscrito
    capital_suscrito = models.FloatField()

    ## Establece el tipo de capital solicitado: capital pagado
    capital_pagado = models.FloatField()

    ## Establece la distribución porcentual del capital suscrito: público nacional
    publico_nacional = models.FloatField()

    ## Establece la distribución porcentual del capital suscrito: público extranjero
    publico_extranjero = models.FloatField()

    ## Establece la distribución porcentual del capital suscrito: privado nacional
    privado_nacional = models.FloatField()

    ## Establece la distribución porcentual del capital suscrito: privado extranjero
    privado_extranjero = models.FloatField()

    ## Establece la ralacion con la Unidad Económica
    unidad_economica = models.ForeignKey(UnidadEconomica)

@python_2_unicode_compatible
class Accionista(models.Model):

    """!
    Clase que gestiona a los accionistas de la Información Mercantil

    @author Lully Troconis (ltroconis at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 03-05-2016
    @version 2.0.0
    """

    ## Establece el rif del accionista
    rif_accionista = models.CharField(
        max_length=10
    )

    ## Establece el nombre del accionista
    razon_social_accionista = models.CharField(
        max_length=45, help_text=_("Nombre del Accionista")
    )

    ## Establece el porcentaje de acciones que posee el accionista
    porcentaje = models.FloatField(
        help_text=_("Porcentaje de accciones que posee el acionista")
    )

    ## Establece el pais de origen del accionista
    pais_origen = models.ForeignKey(Pais)

    ## Establece la ralacion con la Unidad Económica
    unidad_economica = models.ForeignKey(UnidadEconomica)

@python_2_unicode_compatible
class RepresentanteLegal(models.Model):

    """!
    Clase que gestiona al representante legal de la Información Mercantil

    @author Lully Troconis (ltroconis at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 03-05-2016
    @version 2.0.0
    """

    ## Rif del representante legal
    rif_representante = models.CharField(max_length=10)

    ## razón social del representante legal
    razon_social_representante = models.CharField(
        max_length=255, help_text=("Razón Social")
    )

    ## Correo electrónico del representante legal
    correo_electronico = models.CharField(
        max_length=45, help_text=("correo@dssddsd.com")
    )

    ## Número telefónico del representante legal
    telefono = models.CharField(
        max_length=20, help_text=_("Número telefónico de contacto"),
        validators=[
            validators.RegexValidator(
                r'^[\d+-]+$',
                _("Número telefónico inválido. Solo se permiten números, y los signos + o -")
            ),
        ]
    )

    ## Cargo que se selecciona en un select, del representante legal dentro de la Unidad Económica
    cargo = models.CharField(max_length=45)

    ## Cargo que se introduce en un campo de texto del representante legal dentro de la Unidad Económica
    cargo_otros = models.CharField(max_length=45, null=True)

    ## Establece la ralacion con la Unidad Económica
    unidad_economica = models.ForeignKey(UnidadEconomica)

