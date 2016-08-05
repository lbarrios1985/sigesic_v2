"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidad_economica.models
#
# Clases, atributos y métodos para el modelo de datos de los servicios
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres 
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 05-08-2016
# @version 2.0
from django.db import models
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
from base.models import CaevClase, Pais

class TipoServicio(models.Model):
    """!
    Clase que gestiona los datos para los tipos de servicios

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-08-2016
    @version 2.0
    """
    
    ## Nombre del tipo  Servicio
    nombre = models.CharField(max_length=45)

class Servicio(models.Model):
    """!
    Clase que gestiona los datos para el registro de los Servicios

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-08-2016
    @version 2.0
    """
    
    ## Nombre del Servicio
    nombre_servicio = models.CharField(max_length=45)
    
    ## Establece la relación con el código del tipo de servicio
    tipo_servicio = models.ForeignKey(TipoServicio)
    
    ## Establece la relación con el código CAEV
    caev = models.ForeignKey(CaevClase)
    
    ## Cantidad de clientes
    cantidad_clientes = models.IntegerField()
    
    ## Establece la relación con la sub unidad económica
    subunidad = models.ForeignKey(SubUnidadEconomica)
    
        
class ServicioCliente(models.Model):
    """!
    Clase que gestiona los datos para el registro de los Clientes en los Servicios

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-08-2016
    @version 2.0
    """
    
    ## Nombre del Cliente
    nombre = models.CharField(max_length=45)
    
    ## Rif del ciente
    rif = models.CharField(max_length=10)
    
    ## Año del servicio
    anho_servicio = models.IntegerField()
    
    ## Número de servicios prestados por año
    servicio_prestado = models.IntegerField()
    
    ## Precio del servicio
    precio = models.DecimalField(max_digits=20,decimal_places=5)
    
    ## Tipo de moneda
    tipo_moneda = models.CharField(max_length=2)
    
    ## Monto facturado del servicio
    monto_facturado = models.DecimalField(max_digits=20,decimal_places=5)
    
    ## Establece la relación con el país
    pais = models.ForeignKey(Pais)
    
    ## Establece la relación con la producción
    servicio = models.ForeignKey(Servicio)