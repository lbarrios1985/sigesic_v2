from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

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
        max_length=1, choices=NATURALEZA_JURIDICA, help_text=_("Naturaleza Jurídica")
    )

    ## Establece el tipo de capital solicitado: capital suscrito
    capital_suscrito = models.FloatField(
        help_text=_("Ingrese Capital Suscrito")
    )
    ## Establece el tipo de capital solicitado: capital pagado
    capital_pagado = models.FloatField(
        help_text=("fdfdfdf")
    )

    ## Establece el tipo de capital solicitado: capital privado
    capital_privado = models.FloatField()

    ## Establece el tipo de capital solicitado: capital publico
    capital_publico = models.FloatField()

    ## Establece el tipo de capital solicitado: capital nacional
    capital_nacional = models.FloatField()

    ## Establece el tipo de capital solicitado: capital externo
    capital_externo = models.FloatField()

    ##Establece el tipo de persona
    tipo_persona_id = models.CharField(
        max_length=10, help_text=_("ID persona")
    )

    ##Establece el rif del accionista
    rif_accionista = models.CharField(max_length=10)

    ##Establece el nombre del accionista
    nombre = models.CharField(max_length=45)

    ##Establece el porcentaje de acciones que posee el accionista
    porcentaje = models.FloatField()

    class Meta:
        verbose_name = _("Accionista")
        verbose_name_plural = _("Accionistas")
        # ordering = ("CapitalAccionista",)
