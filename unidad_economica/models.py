"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidad_economica.models
#
# Clases, atributos y métodos para el modelo de datos de la unidad económica
# @author Eveli Ramírez (eramirez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres 
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 04-05-2016
# @version 2.0
from __future__ import unicode_literals
from django.core import validators
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from base.constant import TURNO, ESTATUS_NOTIFICACION, ESTATUS_NOTIFICACION_DEFAULT
from base.models import CaevClase, TipoComunal, AnhoRegistro, Pais
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
    nombre_ue = models.CharField(max_length=255)

    ## Razón Social
    razon_social = models.CharField(max_length=255)

    ## La unidad Económica es exportador (si o no)
    exportador= models.BooleanField(default=False)

    ## Número de Seguro Social
    ivss = models.CharField(max_length=20)

    ## Número de contrato social
    snc = models.CharField(max_length=20)

    ## Organización comunal
    orga_comunal = models.BooleanField(default=False)

    ## Establece la relación con el Tipo de Organización Comunal
    tipo_comunal = models.ForeignKey(TipoComunal, null=True)

    ## Casa Matriz de alguna Franquicia
    casa_matriz_franquicia = models.BooleanField(default=False)

    ## Número de Franquicias asociadas a la Unidad Económica
    nro_franquicia = models.IntegerField()
  
    ## Forma parte de una franquicia
    franquiciado = models.BooleanField(default=False)

    ## Código SITUR de la organización comunal
    situr = models.CharField(max_length=45)

    ## Página web de la Unidad Económica
    pagina_web = models.CharField(max_length=50)

    ## Teléfono de contacto de la Unidad Económica
    telefono = models.CharField(
        max_length=20, help_text=_("Número telefónico de contacto con la Unidad Económica"),
        validators=[
            validators.RegexValidator(
                r'^[\d+-]+$',
                _("Número telefónico inválido. Solo se permiten números, y los signos + o -")
            ),
        ]
    )

    ## Correo electrónico de la Unidad Económica
    correo = models.CharField(
        max_length=50, help_text=("correo@dssddsd.com")
    )

    ## Relación entre la Unidad Económica y el usuario
    user = models.ForeignKey(User)

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
    pais_franquicia = models.ForeignKey(Pais)

    ## Establece la relación con la Unidad Económica
    unidad_economica_rif = models.ForeignKey(UnidadEconomica)

@python_2_unicode_compatible
class ActividadCaev(models.Model):
    """!
    Clase que gestiona los datos de actividades CAEV relacionados con la Unidad Económica

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 16-05-2016
    @version 2.0
    """
    ## Establece la relación con el código CAEV
    caev = models.ForeignKey(CaevClase)

    ## Actividad principal de la Unidad Económica
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

    class Meta:
        """!
        Metaclase que permite establecer las propiedades de la clase Notificacion

        @author Ing. Roldan Vargas rvargas at cenditel.gob.ve
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 23-06-2016
        @version 2.0.0
        """
        verbose_name = _("Notificación")
        verbose_name_plural = _("Notificaciones")
        ordering = ("unidad_economica", "estatus")


@python_2_unicode_compatible
class CertificadoRegistro(models.Model):
    """!
    Clase que contiene los datos sobre el certificado de registro en el sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 01-08-2016
    @version 2.0.0
    """

    numero = models.CharField(max_length=32)
    fecha = models.DateField()
    fecha_emision = models.DateTimeField(auto_now=True)
    anho_registro = models.ForeignKey(AnhoRegistro)
    ue = models.ForeignKey(UnidadEconomica)

    class Meta:
        """!
        Metaclase que permite establecer las propiedades de la clase CertificadoRegistro

        @author Ing. Roldan Vargas rvargas at cenditel.gob.ve
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 01-08-2016
        @version 2.0.0
        """
        verbose_name = _("Certificado de Registro")
        verbose_name_plural = _("Certificados de Registro")
        unique_together = [("ue", "anho_registro")]
