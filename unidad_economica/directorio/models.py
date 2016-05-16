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

from base.models import Parroquia

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

class Directorio(models.Model):
    """!
    Clase que gestiona los datos del directorio de direcciones

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-05-2016
    @version 2.0.0
    """

    ## Prefijos permitidos para el primer campo de direcciones
    PREFIJO_UNO_CHOICES = (
        ('AU', _("Autopista")),
        ('AV', _("Avenida")),
        ('CA', _("Carretera")),
        ('CL', _("Calle")),
        ('CR', _("Carrera")),
        ('VR', _("Vereda")),
    )

    ## Prefijos permitidos para el segundo campo de direcciones
    PREFIJO_DOS_CHOICES = (
        ('ED', _("Edificio")),
        ('GA', _("Galpón")),
        ('CC', _("Centro Comercial")),
        ('QT', _("Quinta")),
        ('CA', _("Casa")),
        ('LC', _("Local")),
    )

    ## Prefijos permitidos para el tercer campo de direcciones
    PREFIJO_TRES_CHOICES = (
        ('LC', _("Local")),
        ('OF', _("Oficina")),
        ('AP', _("Apartamento")),
    )

    ## Prefijos permitidos para el cuarto campo de direcciones
    PREFIJO_CUATRO_CHOICES = (
        ('UB', _("Urbanización")),
        ('SC', _("Sector")),
        ('ZN', _("Zona")),
    )
    
    ## Va a contener los prefijos Autopista, Avenida, Carretera, Calle, Carrera, Vereda 
    prefijo_uno = models.CharField(max_length=2, choices=PREFIJO_UNO_CHOICES)
    
    ## Va a contener la descripción de la dirección en el primer prefijo
    direccion_uno = models.CharField(max_length=20)
    
    ## Va a contener los prefijos Edificio, Galpón, Centro Comercial, Quinta, Casa, Local 
    prefijo_dos = models.CharField(max_length=2, choices=PREFIJO_DOS_CHOICES)
    
    ## Va a contener la descripción de la dirección en el segundo prefijo
    direccion_dos = models.CharField(max_length=20)
    
    ## Va a contener los prefijos Local, Oficina, Apartamento 
    prefijo_tres = models.CharField(max_length=2, choices=PREFIJO_TRES_CHOICES)
    
    ## Va a contener la descripción de la dirección en el tercer prefijo
    direccion_tres = models.CharField(max_length=20)
    
    ## Va a contener los prefijos Urbanización, Sector, Zona 
    prefijo_cuatro = models.CharField(max_length=2, choices=PREFIJO_CUATRO_CHOICES)
    
    ## Va a contener la descripción de la dirección en el cuarto prefijo
    direccion_cuatro = models.CharField(max_length=20)

    ## Coordenadas Geográficas (opcional)
    coordenadas = models.CharField(max_length=255, null=True)  # Posteriormente modificar el tipo de campo con GeoDjango a geom = PointField()
    
    ## Muestra si la dirección esta activa o no
    activo = models.BooleanField(default=True)

    ## Contiene la relación con el modelos Parroquia
    parroquia = models.ForeignKey(Parroquia)
