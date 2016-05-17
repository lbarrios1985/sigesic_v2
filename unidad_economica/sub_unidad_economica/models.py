"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.sub_unidad_economica.models
#
# Contiene las clases, atributos y métodos para el modelo de datos de sub unidad económica
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _

from unidad_economica.directorio.models import Directorio

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

class SubUnidadEconomica(models.Model):
    """!
    Clase que gestiona los datos de la subunidad económica

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-05-2016
    @version 2.0.0
    """
    ## Nombre de la subunidad económica
    nombre_sub = models.CharField(max_length=45)
    
     ## Tipo de coordenada de la sub unidad (Se relaciona con el modelo Coordenada)
    #tipo_coordenada =  models.OneToOneField()
    
    ## Coordenada geográfica de la sub unidad
    coordenada_geografica = models.CharField(max_length=45)
    
    ## Telefono de la sub unidad
    telefono = models.CharField(
        max_length=20, help_text=_("Número telefónico de contacto con el usuario"),
    )
    
    ## Tipo de tenencia de la sub unidad. (Se relaciona con el modelo Tenencia)
    #tipo_tenencia_id = models.OneToOneField()
    
    ## Metros cuadrados de la construcción
    m2_contruccion = models.DecimalField(max_digits=20,decimal_places=5)
    
    ## Metros cuadrados del terreno
    m2_terreno = models.DecimalField(max_digits=20,decimal_places=5)
    
    ## Autonomía Eléctrica en porcentaje
    autonomia_electrica = models.DecimalField(max_digits=20,decimal_places=5)
    
    ## Consumo eléctrico promedio en el mes
    consumo_electrico = models.DecimalField(max_digits=20,decimal_places=5)
        
    ## Cantidad de empleados
    cantidad_empleados = models.IntegerField()

    ## Pregunta si la unidad económica presta un servicio
    sede_servicio =  models.BooleanField()
    
class SubUnidadEconomicaProceso(models.Model):
    """!
    Clase que gestiona los datos comunes de las actividades económicas de la sub-unidad 

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 16-05-2016
    @version 2.0.0
    """        
    ## Código CIIU (Se relaciona con el modelo CIIU)
    #codigo_ciiu_id =  models.OneToOneField()
    
    ## Capacidad instalada mensual (campo de texto)
    capacidad_instalada_texto = models.DecimalField(max_digits=20,decimal_places=5,)
    
    ## Capacidad instalada mensual (Unidad de Medida)
    capacidad_instalada_select = models.CharField(max_length=45)
    
    ## Capacidad instalada mensual (campo de texto)
    capacidad_utilizada = models.DecimalField(max_digits=20,decimal_places=5,)
    
    ## Establece la relación con la Sub Unidad Económica
    sub_unidad_economica = models.ForeignKey(SubUnidadEconomica)
    

class SubUnidadEconomicaDirectorio(models.Model):
    """!
    Clase que contiene la relacion entre la Sub Unidad Economica y el Directorio

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 11-05-2016
    @version 2.0.0
    """

    ## Establece la relación con la Sub Unidad Económica
    sub_unidad_economica = models.ForeignKey(SubUnidadEconomica)

    ## Establece la relación con el Directorio
    directorio = models.ForeignKey(Directorio)