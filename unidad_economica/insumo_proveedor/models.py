"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package insumo_proveedor.models
#
# Clases, atributos y métodos para el modelo de datos de los servicios
# @author Hugo Ramirez (hramirez at cenditel.gob.ve)/Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres 
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 14-09-2016
# @version 2.0
from django.db import models
from base.models import Pais, Proveedor, AnhoRegistro
from base.constant import UNIDAD_MEDIDA
from unidad_economica.bienes_prod_comer.models import Producto
# Create your models here.


class Insumo(models.Model):
    """!
    Clase que gestiona los datos para el registro de los insumos del modulo insumo-proveedor

    @author Hugo Ramirez (hramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 14-09-2016
    @version 2.0
    """

    ## Nombre del Producto
    producto = models.ForeignKey(Producto)

    ## Nombre del Insumo
    nombre_insumo = models.CharField(max_length=45)

    ## Establece la Relación con el Código Arancelario
    #codigo_arancelario = models.ForeignKey()
    
class InsumoProduccion(models.Model):
    """!
    Clase que gestiona los datos para el registro de los insumos del modulo insumo-proveedor

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 21-12-2016
    @version 2.0
    """
    ## Relacion con el modelo de Insumo
    insumo = models.ForeignKey(Insumo)
    
    ## Especificación Técnica del Insumo
    especificacion_tecnica = models.CharField(max_length=45)

    ## Marca del Insumo
    marca = models.CharField(max_length=45)

    ## Numero de Proveedores
    numero_proveedor = models.IntegerField()
    
    ## Relacion Insumo-Proveedor
    relacion = models.IntegerField()
    
    ## Año de registro del insumo
    anho_registro = models.ForeignKey(AnhoRegistro)
    

class InsumoProveedor(models.Model):
    """!
    Clase que gestiona los datos para el registro de los proveedores del modulo insumo-proveedor

    @author Hugo Ramirez (hramirez at cenditel.gob.ve)/ Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 14-09-2016
    @version 2.0
    """

    ## Establece la relacion del insumo con proveedor
    proveedor = models.ForeignKey(Proveedor)

    ## Establece la relacion con la producción del insumo
    insumo_produccion = models.ForeignKey(InsumoProduccion)
    
    ## Precio de Compra por unidad en Bs
    precio_compra_bs = models.DecimalField(max_digits=20,decimal_places=5)
    
    ## Precio de Compra por unidad en usd
    precio_compra_usd = models.DecimalField(max_digits=20,decimal_places=5)
    
    ## Cantidad Comprada
    cantidad_comprada = models.IntegerField()
    
    ## Unidad de medida del producto
    unidad_de_medida = models.CharField(max_length=2,choices=UNIDAD_MEDIDA)


