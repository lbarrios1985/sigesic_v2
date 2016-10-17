"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.directorio.models
#
# Contiene las clases, atributos y métodos para el modelo de datos del directorio
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from base.models import Parroquia
from base.constant import (
    PREFIJO_DIRECTORIO_UNO_CHOICES, PREFIJO_DIRECTORIO_DOS_CHOICES, PREFIJO_DIRECTORIO_TRES_CHOICES,
    PREFIJO_DIRECTORIO_CUATRO_CHOICES
)

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


@python_2_unicode_compatible
class TipoCoordenada(models.Model):
    """!
    Clase que gestiona los tipos de coordenadas disponibles

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 23-06-2016
    @version 2.0.0
    """
    tipo = models.CharField(max_length=25)

    class Meta:
        """!
        Metaclase que permite establecer las propiedades de la clase TipoCoordenada

        @author Ing. Roldan Vargas rvargas at cenditel.gob.ve
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 23-06-2016
        @version 2.0.0
        """
        verbose_name = _("Tipo de Coordenada")
        verbose_name_plural = _("Tipos de Coordenadas")

    def __str__(self):
        """!
        Método que muestra la información sobre el tipo de coordenada

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 27-06-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve el tipo de coordenada
        """
        return self.tipo


@python_2_unicode_compatible
class Directorio(models.Model):
    """!
    Clase que gestiona los datos del directorio de direcciones

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-05-2016
    @version 2.0.0
    """

    ## Va a contener los prefijos Autopista, Avenida, Carretera, Calle, Carrera, Vereda
    tipo_vialidad = models.CharField(max_length=2, choices=PREFIJO_DIRECTORIO_UNO_CHOICES)
    
    ## Va a contener la descripción de la dirección en el primer prefijo
    nombre_vialidad = models.CharField(max_length=54)
    
    ## Va a contener los prefijos Edificio, Galpón, Centro Comercial, Quinta, Casa, Local 
    tipo_edificacion = models.CharField(max_length=2, choices=PREFIJO_DIRECTORIO_DOS_CHOICES)
    
    ## Va a contener la descripción de la dirección en el segundo prefijo
    descripcion_edificacion = models.CharField(max_length=54)
    
    ## Va a contener los prefijos Local, Oficina, Apartamento 
    tipo_subedificacion = models.CharField(max_length=2, choices=PREFIJO_DIRECTORIO_TRES_CHOICES)
    
    ## Va a contener la descripción de la dirección en el tercer prefijo
    descripcion_subedificacion = models.CharField(max_length=54)
    
    ## Va a contener los prefijos Urbanización, Sector, Zona 
    tipo_zonificacion = models.CharField(max_length=2, choices=PREFIJO_DIRECTORIO_CUATRO_CHOICES)
    
    ## Va a contener la descripción de la dirección en el cuarto prefijo
    nombre_zona = models.CharField(max_length=54)

    ## Muestra si la dirección esta activa o no
    activo = models.BooleanField(default=True)

    ## Contiene la relación con el modelos Parroquia
    parroquia = models.ForeignKey(Parroquia)

    ## Coordenadas Geográficas (opcional)
    coordenadas = models.CharField(max_length=255, null=True)  # Posteriormente modificar el tipo de campo con GeoDjango a geom = PointField()

    ## Enlace al usuario al cual le corresponda el directorio
    usuario = models.ForeignKey(User)

    class Meta:
        """!
        Metaclase que permite establecer las propiedades de la clase Directorio

        @author Ing. Roldan Vargas rvargas at cenditel.gob.ve
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 23-06-2016
        @version 2.0.0
        """
        verbose_name = _("Directorio")
        verbose_name_plural = _("Directorios")
