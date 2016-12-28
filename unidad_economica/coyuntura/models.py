"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidad_economica.coyuntura.models
#
# Clases, atributos y métodos para el modelo de datos de coyuntura
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres 
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 22-09-2016
# @version 2.0

from django.db import models
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
from unidad_economica.bienes_prod_comer.models import Producto
from base.models import Cliente
from base.constant import UNIDAD_MEDIDA, TIPO_PERIODICIDAD, LISTA_MES, LISTA_TRIMESTRE
# Create your models here.

class Anho(models.Model):
    anho= models.IntegerField()

class Periodicidad(models.Model):
    ## Establece la periodicidad (semanal, mensual, trimestral)
    descripcion= models.CharField(max_length=1, choices=TIPO_PERIODICIDAD)

    ## Establece algún mes del año
    mes= models.CharField(max_length=2, choices=LISTA_MES, null=True)

    ## Establece algún trimestre del año
    trimestre= models.CharField(max_length=2, choices=LISTA_TRIMESTRE, null=True)

    ## Establece el año
    anho= models.ForeignKey(Anho)

class Produccion(models.Model):
    ##cantidad producida
    cantidad_produccion= models.FloatField()

    ## Establece la unidad de medida
    unidad_medida= models.CharField(max_length=2, choices=UNIDAD_MEDIDA)

    ## Número de clientes
    numero_clientes = models.IntegerField()

    ## Establece la relación con la sub unidad económica
    sub_unidad_economica= models.ForeignKey(SubUnidadEconomica)

    ## Establece la relación con bienes_prod_comer
    nombre_producto= models.ForeignKey(Producto, related_name='coyuntura_produccion')

    ## Establece la relación con la periocidad
    periodicidad= models.ForeignKey(Periodicidad)

"""class CantidadCliente(models.Model):
    ## precio en bolivares
    precio_bs= models.FloatField()

    #precio en dolares
    precio_usd= models.FloatField()

    ##Establece el cambio entre divisas
    tipo_cambio_nominal= models.FloatField()

    ## cantidad de productos vendidos
    cantidad_vendida= models.FloatField()

    ## Establece la relación con el cliente
    cliente = models.ForeignKey(Cliente)

    ## Establece la relación con salidaproducto
    salida_producto= models.ForeignKey(SalidaProducto)"""

