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
from django.core.exceptions import ValidationError
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
from base.models import CaevClase, Pais, AnhoRegistro, Cliente
from base.constant import UNIDAD_MEDIDA
import pyexcel

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
    unidad_de_medida = models.CharField(max_length=2,choices=UNIDAD_MEDIDA)
    
    ## Año de registro de la producción
    anho_registro = models.ForeignKey(AnhoRegistro)
    
    ## Cantidad de clientes
    cantidad_clientes = models.IntegerField()
    
    ## Cantidad de insumos
    cantidad_insumos = models.IntegerField()
    
    ## Establece la relación con el producto
    producto = models.ForeignKey(Producto)

    ## Define los campos y validaciones necesarias para el archivo de carga masiva
    cm_fields = [
        {'field': 'id', 'title': str(_("Etiqueta")), 'max_length': 0, 'null': False, 'type': 'string'},
        {
            'field': 'nombre_producto', 'title': str(_("Nombre del Producto")), 'max_length': 45, 'null': False,
            'type': 'string'
        },
        {
            'field': 'especificacion_tecnica', 'title': str(_("Especificación Técnica")), 'max_length': 45,
            'null': False, 'type': 'string'
        },
        {'field': 'marca', 'title': str(_("Marca")), 'max_length': 45, 'null': False, 'type': 'string'},
        {'field': 'caev', 'title': str(_("Código")), 'max_length': 5, 'null': False, 'type': 'string'},
        {'field': 'cantidad_clientes', 'title': str(_("Clientes")), 'max_length': 3, 'null': True, 'type': 'integer'},
        {'field': 'cantidad_insumos', 'title': str(_("Insumos")), 'max_length': 3, 'null': False, 'type': 'integer'},
        {
            'field': 'cantidad_produccion', 'title': str(_("Producción")), 'max_length': 3, 'null': False,
            'type': 'integer'
        },
        {
            'field': 'unidad_de_medida', 'title': str(_("Unidad de Medida")), 'max_length': 2, 'null': False,
            'type': 'string'
        }
    ]
    
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

        datos = []

        if not anho is None and not rel_id is None:
            ## Agrega los datos para el año y sub unidad solicitada
            for prod in Produccion.objects.filter(anho_registro__anho=anho, producto__subunidad_id=rel_id):
                
                codigo = str(prod.producto_id)+" "+str(prod.pk)
                datos.append([
                    codigo, prod.producto.nombre_producto, prod.producto.especificacion_tecnica, prod.producto.marca,
                    prod.producto.caev.pk,prod.cantidad_clientes, prod.cantidad_insumos, prod.cantidad_produccion, prod.unidad_de_medida
                ])

        return {'cabecera': self.cm_fields, 'datos': datos, 'output': 'bienes_prod_comer_produccion'}
    
    def carga_masiva_load(self,path=None, anho=None, rel_id=None):
        """!
        Método para realizar la carga masiva

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 13-12-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param path <b>path</b> Recibe la ruta del archivo para abrir
        @param anho <b>anho</b> Condición que evalúa si extraer los datos del modelo para un año en partícular
        @param rel_id <b>rel_id</b> Tiene el id de la relación del padre
        @return Devuelve el mensaje
        """
        
        load_file = pyexcel.get_sheet(file_name=path)
        ## Se instancia la subunidad
        subunidad = SubUnidadEconomica.objects.get(pk=rel_id)
        ## Se instancia el año de registro
        anho_registro = AnhoRegistro.objects.filter(anho=anho).get()
        ## Se define un arreglo para los errores
        error = []
        for i in range(1,len(load_file.row_range())):
            ## Se busca el producto por el nombre
            producto = Producto.objects.filter(subunidad=rel_id,nombre_producto=load_file[i,1])
            ## Si existe se instancia
            if(producto):
                producto = producto.get()
            ## De lo contrario se crea un nuevo objecto
            else:
                producto = Producto()
                producto.nombre_producto = load_file[i,1]
                producto.especificacion_tecnica = load_file[i,2]
                producto.marca = load_file[i,3]
                caev = CaevClase.objects.get(pk=load_file[i,4])
                producto.caev = caev
                producto.subunidad = subunidad
                ## Se prueba si el modelo es válido
                try:
                    producto.full_clean()
                    producto.save()
                except ValidationError as e:
                    # Do something based on the errors contained in e.message_dict.
                    # Display them to a user, or handle them programmatically.
                    error.append(e.message_dict)
            ## Se crea el modelo de producción
            produccion = Produccion()
            produccion.cantidad_clientes = load_file[i,5]
            produccion.cantidad_insumos = load_file[i,6]
            produccion.cantidad_produccion = load_file[i,7]
            produccion.unidad_de_medida = load_file[i,8]
            produccion.anho_registro = anho_registro
            produccion.producto = producto
            ## Se prueba si el modelo es válido
            try:
                produccion.full_clean()
                produccion.save()
            except ValidationError as e:
                error.append((i,e.message_dict))
        
        ## Si no se registraron errores devuelve el mensaje de los errores
        if(len(error)==0):
            return {'validacion':True,'message':str(_("Se realizó la carga con éxito"))}
        ## En caso contrario retorna los errores
        return {'validacion':False,'message':error}     
        
 
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
    unidad_de_medida = models.CharField(max_length=2,choices=UNIDAD_MEDIDA)
    
    ## Precio de Venta por unidad en Bs
    precio_venta_bs = models.DecimalField(max_digits=20,decimal_places=5)
    
    ## Precio de Venta por unidad en usd
    precio_venta_usd = models.DecimalField(max_digits=20,decimal_places=5)
    
    ## Año de registro de la producción
    anho_registro = models.ForeignKey(AnhoRegistro)
    
    ## Establece la relación con el cliente 
    cliente = models.ForeignKey(Cliente)
    
    ## Establece la relación con la producción
    produccion = models.ForeignKey(Produccion)

    ## Define los campos y validaciones necesarias para el archivo de carga masiva
    cm_fields = [
        {'field': 'id', 'title': str(_("Etiqueta")), 'max_length': 0, 'null': False},
        {'field': 'produccion', 'title': str(_("Nombre del Producto")), 'max_length': 45, 'null': False},
        {'field': 'pais', 'title': str(_("País")), 'max_length': 45, 'null': False},
        {'field': 'nombre', 'title': str(_("Nombre del Cliente")), 'max_length': 45, 'null': False},
        {'field': 'rif', 'title': str(_("R.I.F.")), 'max_length': 5, 'null': True},
        {'field': 'cantidad_vendida', 'title': str(_("Unidades Vendidas")), 'max_length': 3, 'null': False},
        {'field': 'unidad_de_medida', 'title': str(_("Unidad de Medida")), 'max_length': 2, 'null': False},
        {
            'field': 'precio_venta_bs', 'title': str(_("Precio de Venta(Bs)")), 'max_length': 20, 'decimal_places': 5,
            'null': False
        },
        {
            'field': 'precio_venta_usd', 'title': str(_("Precio de Venta(Usd)")), 'max_length': 20, 'decimal_places': 5,
            'null': True
        },
    ]
    
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

        datos = []

        if not anho is None and not rel_id is None:
            ## Agrega los datos para el año y sub unidad solicitada
            for prod in Produccion.objects.filter(anho_registro__anho=anho,producto__subunidad_id=rel_id):
                fact = FacturacionCliente.objects.filter(produccion_id=prod.pk,anho_registro__anho=anho).all()
                ## Si no hay datos devuelve el archivo para llenar
                if not fact:
                    for item in range(prod.cantidad_clientes):
                        datos.append([
                            '', prod.producto.nombre_producto, '' ,'', '', '', '','','',''
                        ])
                ## Si los hay igual cantidades de registros con lo que se marcó inicialmente
                ## se llena normalmente
                elif(len(fact)==prod.cantidad_clientes):
                    for item in fact:
                        datos.append([
                            '', prod.producto.nombre_producto, item.cliente.pais.nombre, item.cliente.nombre,
                            item.cliente.rif,item.cantidad_vendida, item.unidad_de_medida, item.precio_venta_bs,
                            item.precio_venta_usd
                        ])
                ## Si la cantidad de registros es distinta a lo que se marcó inicialmente
                ## se llena con los registros que existan, y se llena con campos vacios lo faltante
                elif(len(fact)!=prod.cantidad_clientes):
                    for item in fact:
                        datos.append([
                            '', prod.producto.nombre_producto, item.cliente.pais.nombre, item.cliente.nombre,
                            item.cliente.rif,item.cantidad_vendida, item.unidad_de_medida, item.precio_venta_bs,
                            item.precio_venta_usd
                        ])
                    for item in range(prod.cantidad_clientes-len(fact)):
                        datos.append([
                            '', prod.producto.nombre_producto, '' ,'', '', '', '','',''
                        ])
                        
        return {'cabecera': self.cm_fields, 'datos': datos, 'output': 'bienes_prod_comer_cliente'}
    
    def carga_masiva_load(self,path=None, anho=None, rel_id=None):
        """!
        Método para realizar la carga masiva

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 14-12-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param path <b>path</b> Recibe la ruta del archivo para abrir
        @param anho <b>anho</b> Condición que evalúa si extraer los datos del modelo para un año en partícular
        @param rel_id <b>rel_id</b> Tiene el id de la relación del padre
        @return Devuelve el mensaje
        """
        
        load_file = pyexcel.get_sheet(file_name=path)
        ## Se instancia la subunidad
        subunidad = SubUnidadEconomica.objects.get(pk=rel_id)
        ## Se instancia el año de registro
        anho_registro = AnhoRegistro.objects.filter(anho=anho).get()
        ## Se define un arreglo para los errores
        error = []
        for i in range(1,len(load_file.row_range())):
            ## Se busca la produccion
            produccion = Produccion.objects.filter(producto__subunidad_id=rel_id,producto__nombre_producto=load_file[i,1]).get()
            ## Se busca el cliente
            cliente = Cliente.objects.filter(rif=load_file[i,4])
            if cliente:
                cliente = cliente.get()
            else:
                pais = Pais.objects.filter(nombre=load_file[i,2]).get()
                ## Se crea y se guarda el modelo de cliente
                cliente = Cliente()
                cliente.nombre = load_file[i,3]
                #Si es venezuela se toma en cuenta el rif
                if(load_file[i,2]=="Venezuela"):
                    cliente.rif = load_file[i,4]
                cliente.pais = pais
                cliente.save()
            ## Se crea la facturacion
            facturacion = FacturacionCliente()
            facturacion.cantidad_vendida = load_file[i,5]
            facturacion.unidad_de_medida = load_file[i,6]
            facturacion.precio_venta_bs = load_file[i,7]
            facturacion.precio_venta_usd = load_file[i,8]
            facturacion.anho_registro = anho_registro
            facturacion.cliente = cliente
            facturacion.produccion = produccion
            try:
                facturacion.full_clean()
                facturacion.save()
            except ValidationError as e:
                error.append((i,e.message_dict))
        
        ## Si no se registraron errores devuelve el mensaje de los errores
        if(len(error)==0):
            return {'validacion':True,'message':str(_("Se realizó la carga con éxito"))}
        ## En caso contrario retorna los errores
        return {'validacion':False,'message':error}     
