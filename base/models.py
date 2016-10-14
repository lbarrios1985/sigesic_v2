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
        """!
        Método que muestra la información sobre el Estado

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 29-06-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve los datos del Estado
        """
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

    def __str__(self):
        """!
        Método que muestra la información sobre el Municipio

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 29-06-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve los datos del Municipio
        """
        return self.nombre


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
        """!
        Método que muestra la información sobre la Parroquia

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 29-06-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve los datos de la Parroquia
        """
        return self.nombre


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
        """!
        Método que muestra la información sobre la Ciudad

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 29-06-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve los datos de la Ciudad
        """
        return self.nombre


@python_2_unicode_compatible
class CaevSeccion(models.Model):
    """!
    Clase que contiene las secciones de Actividades Económicas

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 10-06-2016
    @version 2.0
    """

    ## Código de la Sección
    seccion = models.CharField(max_length=6, primary_key=True)

    ## Descripción del Código de la Sección
    descripcion = models.CharField(max_length=500)


@python_2_unicode_compatible
class CaevDivision(models.Model):
    """!
    Clase que contiene las divisiones de Actividades Económicas

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 10-06-2016
    @version 2.0
    """

    ## Código de la División
    division = models.CharField(max_length=6, primary_key=True)

    ## Descripción del Código de la Divisíon
    descripcion = models.CharField(max_length=500)

    ## Establece la relación con la Sección CAEV
    seccion = models.ForeignKey(CaevSeccion)


@python_2_unicode_compatible
class CaevGrupo(models.Model):
    """!
    Clase que contiene los grupos de Actividades Económicas

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 10-06-2016
    @version 2.0
    """

    ## Código del Grupo
    grupo = models.CharField(max_length=6, primary_key=True)

    ## Descripción del Código del Grupo
    descripcion = models.CharField(max_length=500)

    ## Establece la relación con la División CAEV
    division = models.ForeignKey(CaevDivision)


@python_2_unicode_compatible
class CaevClase(models.Model):
    """!
    Clase que contiene el Código de Actividades Económicas

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 2-06-2016
    @version 2.0
    """

    ## Código de las Clases de Actividades Económicas
    clase = models.CharField(max_length=6, primary_key=True)

    ## Descripción del Código de Clases de Actividades Económicas
    descripcion = models.CharField(max_length=500)

    ## Establece la relación con el Grupo CAEV
    grupo = models.ForeignKey(CaevGrupo)


@python_2_unicode_compatible
class CaevRama(models.Model):
    """!
    Clase que contiene las Ramas de Actividades Económicas

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 10-06-2016
    @version 2.0
    """

    ## Código de la Rama
    rama = models.CharField(max_length=6, primary_key=True)

    ## Descripción del Código de la Rama
    descripcion = models.CharField(max_length=500)

    ## Establece la relación con la Clase CAEV
    clase = models.ForeignKey(CaevClase)


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


@python_2_unicode_compatible
class AnhoRegistro(models.Model):
    """!
    Clase que contiene los Años solicitados para el registro de datos

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 23-06-2016
    @version 2.0.0
    """

    ## Año a registrar
    anho = models.CharField(max_length=4, unique=True)

    class Meta:
        """!
        Metaclase que permite establecer las propiedades de la clase AnhoRegistro

        @author Ing. Roldan Vargas rvargas at cenditel.gob.ve
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 23-06-2016
        @version 2.0.0
        """
        verbose_name = _("Año de Registro")
        verbose_name_plural = _("Años de Registros")

@python_2_unicode_compatible
class Cliente(models.Model):
    """!
    Clase que gestiona los datos para el registro de los Clientes en los Bienes Producidos y comercializados

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 13-07-2016
    @version 2.0
    """
    
    ## Nombre del Cliente
    nombre = models.CharField(max_length=45)
    
    ## Rif del ciente
    rif = models.CharField(max_length=10)
    
    ## Establece la relación con el país
    pais = models.ForeignKey(Pais)