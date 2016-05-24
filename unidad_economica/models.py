"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidad_economica.models
#
# Clases, atributos y métodos para el modelo de datos de la unidad económica
# @author Eveli Ramírez (eramirez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 04-05-2016
# @version 2.0
from __future__ import unicode_literals
from django.core import validators
from django.db import models

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from base.constant import TURNO, ESTATUS_NOTIFICACION, ESTATUS_NOTIFICACION_DEFAULT
from base.models import TipoComunal, Ciiu
from .directorio.models import Directorio

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


@python_2_unicode_compatible
class UnidadEconomica(models.Model):
    """!
    Clase que gestiona los datos para el registro de la Unidad Económica

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 04-05-2016
    @version 2.0
    """

    ## R.I.F. de la Unidad Económica que identifica al usuario en el sistema
    rif = models.CharField(max_length=10)

    ## Nombre Comercial de la Unidad Económica
    nombre_ue = models.CharField(max_length=30)

    ## Razón Social
    razon_social = models.CharField(max_length=45)

    ## Número de Seguro Social
    ivss = models.CharField(max_length=10)

    ## Número de contrato social
    snc = models.CharField(max_length=10)

    ## Número de Plantas Productivas de la Unidad Económica
    nro_planta = models.IntegerField(null=True)

    ## Número de Unidades Comercializadoras
    nro_unid_comercializadora = models.IntegerField(null=True)

    ## Servicios que presta la Unidad Económica
    servicio = models.BooleanField(default=False)

    ## Organización comunal
    orga_comunal = models.BooleanField(default=False)

    ## Establece la relación con el Tipo de Organización Comunal
    tipo_comunal = models.ForeignKey(TipoComunal)

    ## Casa Matriz de alguna Franquicia
    casa_matriz_franquicia = models.BooleanField(default=False)

    ## Número de Franquicias asociadas a la Unidad Económica
    nro_franquicia = models.IntegerField(
        null=True, 
        validators=[
            validators.RegexValidator(
                r'^[\d]+$',
                _("Valor inválido. Solo se permiten números")
            ),
        ],
    )
  
    ## Forma parte de una franquicia
    franquiciado = models.BooleanField(default=False)

    ## Código SITUR de la organización comunal
    codigo_SITUR = models.CharField(max_length=45)

@python_2_unicode_compatible
class Franquicia(models.Model):
    """!
    Clase que gestiona los datos de la franquicia relacionados con la Unidad Económica

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 16-05-2016
    @version 2.0
    """

    ## RIF de la casa matriz de la franquicia
    rif_casa_matriz = models.CharField(max_length=10)

    ## Nombre de la Franquicia 
    nombre_franquicia = models.CharField(max_length=45)

    ## País de origen de la franquicia
    pais_franquicia = models.CharField(max_length=50)

    ## Establece la relación con la Unidad Económica
    unidad_economica_rif = models.ForeignKey(UnidadEconomica)

@python_2_unicode_compatible
class ActividadCiiu(models.Model):
    """!
    Clase que gestiona los datos de actividades CIIU relacionados con la Unidad Económica

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 16-05-2016
    @version 2.0
    """
    ## Establece la relación con el código CIUU
    ciiu = models.ForeignKey(Ciiu)

    principal = models.BooleanField(default=True)

    ## Establece la relación con la Unidad Económica
    unidad_economica_rif = models.ForeignKey(UnidadEconomica)

@python_2_unicode_compatible
class UnidadEconomicaDirectorio(models.Model):
    """!
    Clase que gestiona los datos de dirección asociada a una Unidad Económica

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2016
    @version 2.0.0
    """

    ## Establece la relación con la Unidad Económica
    unidad_economica = models.ForeignKey(UnidadEconomica)

    ## Establece la relación con el Directorio
    directorio = models.ForeignKey(Directorio)


@python_2_unicode_compatible
class Notificacion(models.Model):
    """!
    Clase que gestiona las notificaciones realizadas a los usuarios

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 10-05-2016
    @version 2.0.0
    """

    ## Registra el mensaje de la notificación a enviar
    mensaje = models.TextField(help_text=_("Mensaje"))

    ## Estatus del mensaje
    estatus = models.CharField(max_length=1, choices=ESTATUS_NOTIFICACION, default=ESTATUS_NOTIFICACION_DEFAULT)

    ## Establece la relación con la Unidad Económica a la cual se le envío la notificación
    unidad_economica = models.ForeignKey(UnidadEconomica)