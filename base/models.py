"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace base.models
#
# Contiene las clases, atributos y métodos para el modelo de datos básicos
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.db import models
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from base.constant import TURNO, ESTATUS_NOTIFICACION, ESTATUS_NOTIFICACION_DEFAULT
from unidad_economica.models import UnidadEconomica

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


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


@python_2_unicode_compatible
class Pais(models.Model):
    """!
    Clase que contiene los países

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 10-05-2016
    @version 2.0.0
    """

    ## Nombre del pais
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % self.nombre

    def __unicode__(self):
        return "%s" % self.nombre


@python_2_unicode_compatible
class Estado(models.Model):
    """!
    Clase que contiene los Estados de un Pais

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 10-05-2016
    @version 2.0.0
    """

    ## Nombre del Estado
    nombre = models.CharField(max_length=50)

    ## Pais en donde esta ubicado el Estado
    pais = models.ForeignKey(Pais)

    def __str__(self):
        return "%s" % self.nombre

    def __unicode__(self):
        return "%s" % self.nombre


@python_2_unicode_compatible
class Municipio(models.Model):
    """!
    Clase que contiene los Municipios de un Estado

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 10-05-2016
    @version 2.0.0
    """

    ## Nombre del Municipio
    nombre = models.CharField(max_length=50)

    ## Estado en donde se encuentra el Municipio
    estado = models.ForeignKey(Estado)

    def __str__(self):
        return "%s" % self.nombre

    def __unicode__(self):
        return "%s" % self.nombre


@python_2_unicode_compatible
class Parroquia(models.Model):
    """!
    Clase que contiene las parroquias de un Municipio

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 10-05-2016
    @version 2.0.0
    """

    ## Nombre de la Parroquia
    nombre = models.CharField(max_length=50)

    ## Municipio en el que se encuentra ubicada la Parroquia
    municipio = models.ForeignKey(Municipio)

    def __str__(self):
        return "%s" % self.nombre

    def __unicode__(self):
        return "%s" % self.nombre


@python_2_unicode_compatible
class Ciudad(models.Model):
    """!
    Clase que contiene las Ciudades de un Estado

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 10-05-2016
    @version 2.0.0
    """

    ## Nombre de la Ciudad
    nombre = models.CharField(max_length=50)

    ## Estado en donde se encuentra ubicada la Ciudad
    estado = models.ForeignKey(Estado)

    def __str__(self):
        return "%s" % self.nombre

    def __unicode__(self):
        return "%s" % self.nombre