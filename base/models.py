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

from base.constant import TURNO

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


@python_2_unicode_compatible
class DatosSistema(models.Model):
    """!
    Clase que gestiona los datos básicos del sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 04-05-2016
    @version 2.0.0
    """

    ## Nombre de la institución que gestiona el sistema
    institucion = models.CharField(max_length=250)

    ## Dirección de ubicación de la institución que gestiona el sistema
    direccion = models.TextField()

    ## Dirección de ubicación de la institución que gestiona el sistema (continuación)
    direccion_otra = models.TextField(null=True, default=None)

    ## Logotipo del sistema
    logo = models.ImageField(upload_to='./static/img/')

    ## Logotipo corto para el sistema a mostrar cuando se oculta la barra de menú lateral
    logo_short = models.ImageField(upload_to='./static/img/')

    ## Indica si el registro esta activo
    activo = models.BooleanField(default=True)


@python_2_unicode_compatible
class TelefonoSistema(models.Model):
    """!
    Clase que gestiona los datos de teléfonos de contacto del sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 04-05-2016
    @version 2.0.0
    """

    ## Codigo del pais
    codigo_pais = models.CharField(max_length=4)

    ## Codigo de area
    codigo_area = models.CharField(max_length=3)

    ## Numero telefonico
    numero = models.CharField(max_length=8)

    ## Relacion con los datos basicos del sistema
    datos_sistema = models.ForeignKey(DatosSistema)


@python_2_unicode_compatible
class HorarioSistema(models.Model):
    """!
    Clase que gestiona los datos de atención al público del sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 04-05-2016
    @version 2.0.0
    """

    ## Hora inicial de atencion al publico
    hora_inicial = models.CharField(max_length=8)

    ## Hora final de atencion al publico
    hora_final = models.CharField(max_length=8)

    ## Turno de atencion al publico (M)añana o (T)arde
    turno = models.CharField(max_length=1, choices=TURNO)

    ## Indica si el turno esta o no activo
    activo = models.BooleanField(default=True)

    ## Relacion con los datos basicos del sistema
    datos_sistema = models.ForeignKey(DatosSistema)


@python_2_unicode_compatible
class ImagenCarousel(models.Model):
    """!
    Clase que gestiona los datos del carousel a mostrar en la pantalla de acceso al sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 04-05-2016
    @version 2.0.0
    """

    ## Ruta de la imagen a mostrar en el carousel
    imagen = models.ImageField(upload_to='./static/img/')

    ## Título de la imagen a mostrar en el carousel
    titulo = models.CharField(max_length=40)

    ## Descripción de la imagen a mostrar en el carousel
    descripcion = models.TextField()

    ## Relacion con los datos basicos del sistema
    datos_sistema = models.ForeignKey(DatosSistema)