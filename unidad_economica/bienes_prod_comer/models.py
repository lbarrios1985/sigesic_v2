"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidad_economica.models
#
# Clases, atributos y métodos para el modelo de datos de los bienes producidos y comercializados
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres 
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 13-07-2016
# @version 2.0
from django.db import models
from django.utils.translation import ugettext_lazy as _
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
from base.models import CaevClase, Pais, AnhoRegistro
from base.constant import UNIDAD_MEDIDA

class Producto(models.Model):
    """!
    Clase que gestiona los datos para el registro de los Productos en los Bienes Producidos y comercializados

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 13-07-2016
    @version 2.0
    """
    
    ## Nombre del Producto
    nombre_producto = models.CharField(max_length=45)
    
    ## Marca del Producto
    marca = models.CharField(max_length=45)
    
    ## Especificación Técnica del Producto
    especificacion_tecnica = models.CharField(max_length=45)
    
    ## Establece la relación con el código CAEV
    caev = models.ForeignKey(CaevClase)
    
    ## Establece la relación con la sub unidad económica
    subunidad = models.ForeignKey(SubUnidadEconomica)
   
class Produccion(models.Model):
    """!
    Clase que gestiona los datos para el registro de la Produccion en los Bienes Producidos y comercializados

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 13-07-2016
    @version 2.0
    """
    
    ## Cantidad Producida
    cantidad_produccion = models.IntegerField()
    
    ## Unidad de medida del producto
    unidad_de_medida = models.CharField(max_length=2)
    
    ## Año de registro de la producción
    anho_registro = models.ForeignKey(AnhoRegistro)
    
    ## Cantidad de clientes
    cantidad_clientes = models.IntegerField()
    
    ## Cantidad de insumos
    cantidad_insumos = models.IntegerField()
    
    ## Establece la relación con el producto
    producto = models.ForeignKey(Producto)
    
    def carga_masiva_init(self, anho=None, rel_id=None):
        """!
        Método que establece los parámetros a mostrar con su rerspectiva información en los archivos de carga masiva

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 11-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param anho <b>anho</b> Condición que evalúa si extraer los datos del modelo para un año en partícular
        @param rel_id <b>rel_id</b> Tiene el id de la relación del padre
        @return Devuelve los campos del archivo de carga masiva
            {
                'field': 'id',
                'title': str(_("Etiqueta")),
                'max_length': 0,
                'null': False,
                'type': 'string'
            },
        """

        ## Define los campos y validaciones necesarias para el archivo de carga masiva
        fields = [
            {
                'field': 'id',
                'title': str(_("Etiqueta")),
                'max_length': 0,
                'null': False,
                'related':True,
                'depend':False,
                'related_model':'Producto',
                'type': 'string'
            },
            {
                'field': 'nombre_producto',
                'title': str(_("Nombre del Producto")),
                'max_length': 45,
                'null': False,
                'related':True,
                'depend':False,
                'related_model':'Producto',
                'type': 'string'
            },
            {
                'field': 'especificacion_tecnica',
                'title': str(_("Especificación Técnica")),
                'max_length': 45,
                'null': False,
                'related':True,
                'depend':False,
                'related_model':'Producto',
                'type': 'string'
            },
            {
                'field': 'marca',
                'title': str(_("Marca")),
                'max_length': 45,
                'null': False,
                'related':True,
                'depend':False,
                'related_model':'Producto',
                'type': 'string'
            },
            {
                'field': 'caev',
                'title': str(_("Código")),
                'max_length': 5,
                'null': False,
                'related':True,
                'depend':True,
                'related_app':'base',
                'related_model':'CaevClase',
                'type': 'string'
            },
            {
                'field': 'cantidad_clientes',
                'title': str(_("Clientes")),
                'max_length': 3,
                'null': True,
                'related':False,
                'depend':False,
                'type': 'integer'
            },
            {
                'field': 'cantidad_insumos',
                'title': str(_("Insumos")),
                'max_length': 3,
                'null': False,
                'related':False,
                'depend':False,
                'type': 'integer'
            },
            {
                'field': 'cantidad_produccion',
                'title': str(_("Producción")),
                'max_length': 3,
                'null': False,
                'related':False,
                'depend':False,
                'type': 'integer'
            },
            {
                'field': 'unidad_de_medida',
                'title': str(_("Unidad de Medida")),
                'max_length': 2,
                'null': False,
                'related':False,
                'depend':False,
                'type': 'string'
            }
        ]

        datos = []
        relation = {}

        if not anho is None and not rel_id is None:
            ## Agrega los datos para el año y sub unidad solicitada
            for prod in Produccion.objects.filter(anho_registro__anho=anho, producto__subunidad_id=rel_id):
                dic_um = dict(UNIDAD_MEDIDA)
                unidad_medida = str(dic_um.get(prod.unidad_de_medida))
                
                codigo = str(prod.producto_id)+" "+str(prod.pk)
                datos.append([
                    codigo, prod.producto.nombre_producto, prod.producto.especificacion_tecnica, prod.producto.marca,
                    prod.producto.caev.pk,prod.cantidad_clientes, prod.cantidad_insumos, prod.cantidad_insumos,
                    prod.cantidad_produccion, unidad_medida
                ])
            relation = {
                'padre':{
                    'app':'sub_unidad_economica',
                    'mod':'SubUnidadEconomica',
                    'field':'subunidad',
                    'child':'Producto',
                    'instance': SubUnidadEconomica.objects.get(pk=rel_id)
                },
                'relation_model':{
                    'app':'bienes_prod_comer',
                    'mod':'Producto',
                    'field':'producto'
                },
            }
        return {'cabecera': fields, 'datos': datos, 'output': 'bienes_prod_comer_produccion', 'relation':relation}

    
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
    
    ## Establece la relación con la producción
    produccion = models.ForeignKey(Produccion)
    
class FacturacionCliente(models.Model):
    """!
    Clase que gestiona los datos para el registro de la Produccion que se necesita del cliente en los Bienes Producidos y comercializados

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 13-07-2016
    @version 2.0
    """
    
    ## Cantidad Vendida
    cantidad_vendida = models.IntegerField()
    
    ## Unidad de medida del producto
    unidad_de_medida = models.CharField(max_length=2)
    
    ## Precio de Venta por unidad en Bs
    precio_venta_bs = models.DecimalField(max_digits=20,decimal_places=5)
    
    ## Precio de Venta por unidad en usd
    precio_venta_usd = models.DecimalField(max_digits=20,decimal_places=5)
    
    ## Tipo de cambio
    tipo_cambio = models.DecimalField(max_digits=20,decimal_places=5)
    
    ## Año de registro de la producción
    anho_registro = models.ForeignKey(AnhoRegistro)
    
    ## Establece la relación con el producto 
    cliente = models.ForeignKey(Cliente)
    
    ## Establece la relación con el producto
    producto = models.ForeignKey(Producto)
    
    def carga_masiva_init(self, anho=None, rel_id=None):
        """!
        Método que establece los parámetros a mostrar con su rerspectiva información en los archivos de carga masiva

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 11-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param anho <b>anho</b> Condición que evalúa si extraer los datos del modelo para un año en partícular
        @param rel_id <b>rel_id</b> Tiene el id de la relación del padre
        @return Devuelve los campos del archivo de carga masiva
            {
                'field': 'id',
                'title': str(_("Etiqueta")),
                'max_length': 0,
                'null': False,
                'type': 'string'
            },
        """

        ## Define los campos y validaciones necesarias para el archivo de carga masiva
        fields = [
            {
                'field': 'id',
                'title': str(_("Etiqueta")),
                'max_length': 0,
                'null': False,
                'related':True,
                'depend':False,
                'related_model':'Cliente',
                'type': 'string'
            },
            {
                'field': 'producto',
                'title': str(_("Nombre del Producto")),
                'max_length': 45,
                'null': False,
                'related':True,
                'depend':True,
                'related_app':'bienes_prod_comer',
                'related_model':'Produccion',
                'need_object':True,
                'filtro':'producto__nombre_producto',
                'ambigous':True,
                'amb_app':'bienes_prod_comer',
                'amb_model':'Producto',
                'amb_filter':'pk',
                'amb_field':'producto_id',
                'type': 'string'
            },
            {
                'field': 'pais',
                'title': str(_("País")),
                'max_length': 45,
                'null': False,
                'related':True,
                'depend':True,
                'related_app':'base',
                'related_model':'Pais',
                'need_object':True,
                'filtro':'nombre',
                'type': 'string'
            },
            {
                'field': 'nombre',
                'title': str(_("Nombre del Cliente")),
                'max_length': 45,
                'null': False,
                'related':True,
                'depend':False,
                'related_model':'Cliente',
                'type': 'string'
            },
            {
                'field': 'rif',
                'title': str(_("Rif")),
                'max_length': 5,
                'null': True,
                'related':True,
                'depend':False,
                'related_model':'Cliente',
                'type': 'string'
            },
            {
                'field': 'cantidad_produccion',
                'title': str(_("Unidades Vendidas")),
                'max_length': 3,
                'null': False,
                'related':False,
                'depend':False,
                'type': 'integer'
            },
            {
                'field': 'unidad_de_medida',
                'title': str(_("Unidad de Medida")),
                'max_length': 2,
                'null': False,
                'related':False,
                'depend':False,
                'type': 'string'
            },
            {
                'field': 'precio_venta_bs',
                'title': str(_("Precio de Venta(Bs)")),
                'max_length': 20,
                'decimal_places':5,
                'null': False,
                'related':False,
                'depend':False,
                'type': 'double'
            },
            {
                'field': 'precio_venta_usd',
                'title': str(_("Precio de Venta(Usd)")),
                'max_length': 20,
                'decimal_places':5,
                'null': True,
                'related':False,
                'depend':False,
                'type': 'double'
            },
            {
                'field': 'tipo_cambio',
                'title': str(_("Tipo de Cambio")),
                'max_length': 20,
                'decimal_places':5,
                'null': True,
                'related':False,
                'depend':False,
                'type': 'double'
            },
        ]

        datos = []
        relation = {}

        if not anho is None and not rel_id is None:
            ## Agrega los datos para el año y sub unidad solicitada
            dic_um = dict(UNIDAD_MEDIDA)
            for prod in Produccion.objects.filter(anho_registro__anho=anho,producto__subunidad_id=rel_id):
                fact = FacturacionCliente.objects.filter(producto=prod.pk)
                for item in range(prod.cantidad_clientes):
                    #codigo = str(fact.producto_id)+" "+str(fact.pk)
                    if fact:
                        unidad_medida = str(dic_um.get(fact.unidad_de_medida))
                        datos.append([
                            '', prod.producto.nombre_producto, prod.producto.especificacion_tecnica, prod.producto.marca,
                            prod.producto.caev.pk,prod.cantidad_clientes, prod.cantidad_insumos, prod.cantidad_insumos,
                            prod.cantidad_produccion, unidad_medida
                        ])
                    else:
                        datos.append([
                            '', prod.producto.nombre_producto, '' ,'', '', '', '','','',''
                        ])
                        
            relation = {
                'padre':{
                    'app':'bienes_prod_comer',
                    'mod':'Produccion',
                    'field':'produccion',
                    'child':'Cliente',
                    'instance':''
                },
                'relation_model':{
                    'app':'bienes_prod_comer',
                    'mod':'Cliente',
                    'field':'cliente'
                },
            }
        return {'cabecera': fields, 'datos': datos, 'output': 'bienes_prod_comer_cliente', 'relation':relation}
