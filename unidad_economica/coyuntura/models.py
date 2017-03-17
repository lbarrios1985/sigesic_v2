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
from base.constant import UNIDAD_MEDIDA
from django.utils.translation import ugettext_lazy as _

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

## Tipo de Periodicidad
TIPO_PERIODICIDAD = (
    ('S',_('Semanal')),
    ('M',_('Mensual')),
    ('T',_('Trimestral')),
)

## Lista de Meses
LISTA_MES = (
    ('EN',_('Enero')),
    ('FE',_('Febrero')),
    ('MA',_('Marzo')),
    ('AB',_('Abril')),
    ('MY',_('Mayo')),
    ('JN',_('Junio')),
    ('JL',_('Julio')),
    ('AG',_('Agosto')),
    ('SE',_('Septiembre')),
    ('OC',_('Octubre')),
    ('NO',_('Noviembre')),
    ('DI',_('Diciembre')),
)

## Lista de Trimestres
LISTA_TRIMESTRE = (
    ('T1',_('Trimestre 1')),
    ('T2',_('Trimestre 2')),
    ('T3',_('Trimestre 3')),
    ('T4',_('Trimestre 4')),
)

## Valor semanal (se necesitaba asi para que funcionara) se requiere cambios a futuro
SEMANAL = (
    (None,_('')),
    ('S',_('Semanal')),
)

## Valor mensual (se necesitaba asi para que funcionara) se requiere cambios a futuro
MENSUAL = (
    (None,_('')),
    ('M',_('Mensual')),
)

## Valor trimestral (se necesitaba asi para que funcionara) se requiere cambios a futuro
TRIMESTRAL = (
    (None,_('')),
    ('T',_('Trimestral')),
)

## Valor del mes de enero, se hizo lo mismo con todos los meses. Requiere cambios a futuro
ENERO = (
    (None,_('')),
    ('EN',_('Enero')),
)
FEBRERO = (
    (None,_('')),
    ('FE',_('Febrero')),
)
MARZO = (
    (None,_('')),
    ('MA',_('Marzo')),
)
ABRIL = (
    (None,_('')),
    ('AB',_('Abril')),
)
MAYO = (
    (None,_('')),
    ('MY',_('Mayo')),
)
JUNIO = (
    (None,_('')),
    ('JN',_('Junio')),
)
JULIO = (
    (None,_('')),
    ('JL',_('Julio')),
)
AGOSTO = (
    (None,_('')),
    ('AG',_('Agosto')),
)
SEPTIEMBRE = (
    (None,_('')),
    ('SE',_('Septiembre')),
)
OCTUBRE = (
    (None,_('')),
    ('OC',_('Octubre')),
)
NOVIEMBRE = (
    (None,_('')),
    ('NO',_('Noviembre')),
)
DICIEMBRE = (
    (None,_('')),
    ('DI',_('Diciembre')),
)

## Valor del trimestre 1, se hizo lo mismo con todos los trimestres. Requiere cambios a futuro
TRIMESTRE_1 = (
    (None,_('')),
    ('T1',_('Trimestre 1')),
)
TRIMESTRE_2 = (
    (None,_('')),
    ('T2',_('Trimestre 2')),
)
TRIMESTRE_3 = (
    (None,_('')),
    ('T3',_('Trimestre 3')),
)
TRIMESTRE_4 = (
    (None,_('')),
    ('T4',_('Trimestre 4')),
)

class MesAdmin(models.Model):
    """!
    Clase que gestiona los meses de la periodicidad en la parte del administrador

    @author wpaez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 09-01-2017
    @version 2.0
    """

    enero= models.CharField(max_length=2, choices=ENERO, null=True)
    febrero= models.CharField(max_length=2, choices=FEBRERO, null=True)
    marzo= models.CharField(max_length=2, choices=MARZO, null=True)
    abril= models.CharField(max_length=2, choices=ABRIL, null=True)
    mayo= models.CharField(max_length=2, choices=MAYO, null=True)
    junio= models.CharField(max_length=2, choices=JUNIO, null=True)
    julio= models.CharField(max_length=2, choices=JULIO, null=True)
    agosto= models.CharField(max_length=2, choices=AGOSTO, null=True)
    septiembre= models.CharField(max_length=2, choices=SEPTIEMBRE, null=True)
    octubre= models.CharField(max_length=2, choices=OCTUBRE, null=True)
    noviembre= models.CharField(max_length=2, choices=NOVIEMBRE, null=True)
    diciembre= models.CharField(max_length=2, choices=DICIEMBRE, null=True)
    def __str__(self):
        return '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (self.enero,self.febrero,self.marzo,self.abril,self.mayo,self.junio,self.julio,
        self.agosto,self.septiembre,self.octubre,self.noviembre,self.diciembre)

class TrimestreAdmin(models.Model):
    """!
    Clase que gestiona los trimestres de l periodicidad en la parte del administrador

    @author wpaez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 09-01-2017
    @version 2.0
    """

    trimestre_1= models.CharField(max_length=2, choices=TRIMESTRE_1, null=True)
    trimestre_2= models.CharField(max_length=2, choices=TRIMESTRE_2, null=True)
    trimestre_3= models.CharField(max_length=2, choices=TRIMESTRE_3, null=True)
    trimestre_4= models.CharField(max_length=2, choices=TRIMESTRE_4, null=True)
    def __str__(self):
        return '%s,%s,%s,%s' % (self.trimestre_1,self.trimestre_2,self.trimestre_3,self.trimestre_4)

class AnhoAdmin(models.Model):
    """!
    Clase que gestiona los años de la periodicidad en la parte del administrador

    @author wpaez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 09-01-2017
    @version 2.0
    """
    anho= models.IntegerField()
    def __str__(self):
        return str(self.anho)

#Modelo para llevar el control de periodicidad en la parte del administrador
class PeriodicidadAdmin(models.Model):
    """!
    Clase que gestiona la periodicidad en la parte del administrador

    @author wpaez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 09-01-2017
    @version 2.0
    """

    ## Establece el tipo de periodicidad (semanal, mensual, trimestral)
    periodo= models.CharField(max_length=1, choices=TIPO_PERIODICIDAD)

    ## Establece la relacion con MesAdmin
    mes= models.ForeignKey(MesAdmin, null=True)

    ## Establece la relacion con TrimestreAdmin
    trimestre= models.ForeignKey(TrimestreAdmin, null=True)

    ## Establece la relación con AnhoAdmin
    anho= models.ForeignKey(AnhoAdmin)

    ## Establece la relación con SubUnidadEconomica
    sub_unidad_economica= models.ForeignKey(SubUnidadEconomica)

class Periodicidad(models.Model):
    """!
    Clase que gestiona la periodicidad en la parte del usuario

    @author wpaez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 09-01-2017
    @version 2.0
    """

    ## Establece la periodicidad (semanal, mensual, trimestral)
    periodo= models.CharField(max_length=1, choices=TIPO_PERIODICIDAD)

    ## Establece algún mes del año
    mes= models.CharField(max_length=2, choices=LISTA_MES, null=True)

    ## Establece algún trimestre del año
    trimestre= models.CharField(max_length=2, choices=LISTA_TRIMESTRE, null=True)

    ## Establece el año
    anho= models.IntegerField()

class Produccion(models.Model):
    """!
    Clase que gestiona los datos para el registro de la producción en coyuntura

    @author wpaez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 09-01-2017
    @version 2.0
    """

    ## cantidad producida
    cantidad_produccion= models.FloatField()

    ## Establece la unidad de medida
    unidad_medida= models.CharField(max_length=2, choices=UNIDAD_MEDIDA)

    ## Número de clientes
    numero_clientes = models.IntegerField()

    ## Establece la relación con la sub unidad económica
    sub_unidad_economica= models.ForeignKey(SubUnidadEconomica)

    ## Establece la relación con el Producto de bienes_prod_comer
    producto= models.ForeignKey(Producto, related_name='coyuntura_produccion')

    ## Establece la relación con la periodicidad
    periodicidad= models.ForeignKey(Periodicidad)

class Clientes(models.Model):
    """!
    Clase que gestiona los datos para el registro de clientes en coyuntura

    @author wpaez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 09-01-2017
    @version 2.0
    """

    ## cantidad de productos vendidos
    cantidad_vendida= models.FloatField()

    ## Establece la unidad de medida
    unidad_medida= models.CharField(max_length=2, choices=UNIDAD_MEDIDA)

    ## precio en bolivares
    precio_bs= models.FloatField()

    #precio en dolares
    precio_usd= models.FloatField()

    ## Establece la relación con el cliente
    cliente = models.ForeignKey(Cliente)

    ## Establece la relación con la Producción
    produccion= models.ForeignKey(Produccion)
