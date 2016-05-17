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

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


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
        return self.nombre


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

@python_2_unicode_compatible
class Ciiu(models.Model):
    """!
    Clase que contiene el Código Industrial Internacional de Actividades Económicas

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 17-05-2016
    @version 2.0
    """

    ## Código Industrial Internacional de Actividades Económicas
    codigo_ciiu = models.CharField(max_length=6)

    ## Descripción del Código Industrial Internacional de Actividades Económicas
    descripcion = models.CharField(max_length=45)

    ## Sección
    seccion = models.CharField(max_length=1)

    ## Descripción de la sección
    descripcion_seccion = models.CharField(max_length=45)

    ## División
    division = models.CharField(max_length=3)

    ## Descripción de la División
    descripcion_division = models.CharField(max_length=45)

    ## Grupo
    grupo = models.CharField(max_length=4)

    ## Descripción del grupo
    descripcion_grupo = models.CharField(max_length=45)

@python_2_unicode_compatible
class TipoComunal(models.Model):
    """!
    Clase que contiene los tipos de organizaciones comunales

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 17-05-2016
    @version 2.0
    """

    ## Tipo de Organización Comunal
    tipo_comunal = models.CharField(max_length=45)