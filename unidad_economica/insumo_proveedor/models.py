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
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models import Pais, Proveedor, AnhoRegistro
from base.constant import UNIDAD_MEDIDA
from unidad_economica.bienes_prod_comer.models import Producto, Produccion
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
import pyexcel


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
    
    ## País de origen del insumo
    pais_origen = models.ForeignKey(Pais)
    
    ## Año de registro del insumo
    anho_registro = models.ForeignKey(AnhoRegistro)

    ## Define los campos y validaciones necesarias para el archivo de carga masiva
    cm_fields = [
        {'field': 'id', 'title': str(_("Etiqueta")), 'max_length': 0, 'null': False, 'type': 'string'},
        {
            'field': 'producto', 'title': str(_("Nombre del Producto")), 'max_length': 45, 'null': False,
            'type': 'string'
        },
        {
            'field': 'nombre_insumo', 'title': str(_("Nombre del Insumo")), 'max_length': 45, 'null': False,
            'type': 'string'
        },
        {
            'field': 'especificacion_tecnica', 'title': str(_("Especificación Técnica")), 'max_length': 45,
            'null': False, 'type': 'string'
        },
        {'field': 'marca', 'title': str(_("Marca")), 'max_length': 45, 'null': False, 'type': 'string'},
        # {'field': 'caev', 'title': str(_("Código")), 'max_length': 5, 'null': False, 'type': 'string'},
        {'field': 'relacion', 'title': str(_("Insumo-Proveedor")), 'max_length': 3, 'null': True, 'type': 'integer'},
        {
            'field': 'numero_proveedor', 'title': str(_("# Proveedores")), 'max_length': 3, 'null': False,
            'type': 'integer'
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
            #for ins in InsumoProduccion.objects.filter(anho_registro__anho=anho, insumo__producto__subunidad_id=rel_id):
                ins = InsumoProduccion.objects.filter(insumo__producto_id=prod.producto_id).all()
                ## Si no hay datos devuelve el archivo para llenar
                if not ins:
                    for item in range(prod.cantidad_insumos):
                        datos.append([
                            '', prod.producto.nombre_producto, '' ,'', '', '', ''
                        ])
                ## Si los hay igual cantidades de registros con lo que se marcó inicialmente
                ## se llena normalmente
                elif(len(ins)==prod.cantidad_insumos):
                    for item in ins:
                        datos.append([
                            '', item.insumo.producto.nombre_producto, item.insumo.nombre_insumo, item.especificacion_tecnica,
                            item.marca, item.relacion, item.pais_origen, item.numero_proveedor
                        ])
                ## Si la cantidad de registros es distinta a lo que se marcó inicialmente
                ## se llena con los registros que existan, y se llena con campos vacios lo faltante
                elif(len(ins)!=prod.cantidad_insumos):
                    for item in ins:
                        datos.append([
                            '', item.insumo.producto.nombre_producto, item.insumo.nombre_insumo, item.especificacion_tecnica,
                            item.marca, item.relacion, item.pais_origen, item.numero_proveedor
                        ])
                    for item in range(prod.cantidad_insumos-len(ins)):
                        datos.append([
                            '', prod.producto.nombre_producto, '' ,'', '', '', ''
                        ])

        return {'cabecera': self.cm_fields, 'datos': datos, 'output': 'insumo'}
    
    def carga_masiva_load(self,path=None, anho=None, rel_id=None):
        """!
        Método para realizar la carga masiva

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 22-12-2016
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
            ##Se instancia el Producto
            producto = Producto.objects.get(subunidad_id=rel_id,nombre_producto=load_file[i,1])
            ## Se busca el insumo por el nombre
            insumo = Insumo.objects.filter(producto__subunidad=rel_id,nombre_insumo=load_file[i,2])
            ## Si existe se instancia
            if(insumo):
                insumo = insumo.get()
            ## De lo contrario se crea un nuevo objecto
            else:
                insumo = Insumo()
                insumo.nombre_insumo = load_file[i,2]
                insumo.producto = producto
                ## Se prueba si el modelo es válido
                try:
                    insumo.full_clean()
                    insumo.save()
                except ValidationError as e:
                    error.append(e.message_dict)
            ## Se crea el modelo de insumo_producción
            produccion = InsumoProduccion()
            produccion.especificacion_tecnica = load_file[i,3]
            produccion.marca = load_file[i,4]
            produccion.relacion = load_file[i,5]
            produccion.numero_proveedor = load_file[i,6]
            produccion.anho_registro = anho_registro
            produccion.insumo = insumo
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

    ## Define los campos y validaciones necesarias para el archivo de carga masiva
    cm_fields = [
        {'field': 'id', 'title': str(_("Etiqueta")), 'max_length': 0, 'null': False, 'type': 'string'},
        {
            'field': 'producto', 'title': str(_("Nombre del Producto")), 'max_length': 45, 'null': False,
            'type': 'string'
        },
        {
            'field': 'nombre_insumo', 'title': str(_("Nombre del Insumo")), 'max_length': 45, 'null': False,
            'type': 'string'
        },
        {'field': 'pais', 'title': str(_("Ubicación")), 'max_length': 45, 'null': False, 'type': 'string'},
        {
            'field': 'nombre_proveedor', 'title': str(_("Nombre del Proveedor")), 'max_length': 45, 'null': False,
            'type': 'string'
        },
        {'field': 'rif', 'title': str(_("R.I.F.")), 'max_length': 10, 'null': True, 'type': 'string'},
        {
            'field': 'precio_compra_bs', 'title': str(_("Precio de Compra (Bs)")), 'max_length': 20,
            'decimal_places': 5, 'null': False, 'type': 'decimal'
        },
        {
            'field': 'precio_compra_usd', 'title': str(_("Precio de Compra (Usd)")), 'max_length': 20,
            'decimal_places': 5, 'null': False, 'type': 'decimal'
        },
        {
            'field': 'cantidad_comprada', 'title': str(_("Cantidad Comprada")), 'max_length': 3, 'null': False,
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
            for prod in InsumoProduccion.objects.filter(anho_registro__anho=anho,insumo__producto__subunidad_id=rel_id):
            #for ins in InsumoProduccion.objects.filter(anho_registro__anho=anho, insumo__producto__subunidad_id=rel_id):
                prove = InsumoProveedor.objects.filter(insumo_produccion_id=prod.pk).all()
                ## Si no hay datos devuelve el archivo para llenar
                if not prove:
                    for item in range(prod.numero_proveedor):
                        datos.append([
                            '', prod.insumo.producto.nombre_producto, prod.insumo.nombre_insumo ,'', '', '', '',
                            '', '', ''
                        ])
                ## Si los hay igual cantidades de registros con lo que se marcó inicialmente
                ## se llena normalmente
                elif(len(prove)==prod.numero_proveedor):
                    for item in prove:
                        datos.append([
                            '', item.insumo_produccion.insumo.producto.nombre_producto, item.insumo_produccion.insumo.nombre_insumo,
                            item.proveedor.pais.nombre, item.proveedor.nombre, item.proveedor.rif, item.precio_compra_bs,
                            item.precio_compra_usd, item.cantidad_comprada, item.unidad_de_medida
                        ])
                ## Si la cantidad de registros es distinta a lo que se marcó inicialmente
                ## se llena con los registros que existan, y se llena con campos vacios lo faltante
                elif(len(prove)!=prod.numero_proveedor):
                    for item in prove:
                        datos.append([
                            '', item.insumo_produccion.insumo.producto.nombre_producto, item.insumo_produccion.insumo.nombre_insumo,
                            item.proveedor.pais.nombre, item.proveedor.nombre, item.proveedor.rif, item.precio_compra_bs,
                            item.precio_compra_usd, item.cantidad_comprada, item.unidad_de_medida
                        ])
                    for item in range(prod.cantidad_insumos-len(prove)):
                        datos.append([
                            '', prod.insumo.producto.nombre_producto, prod.insumo.nombre_insumo ,'', '', '', '',
                            '', '', ''
                        ])

        return {'cabecera': self.cm_fields, 'datos': datos, 'output': 'proveedor'}
    
    def carga_masiva_load(self,path=None, anho=None, rel_id=None):
        """!
        Método para realizar la carga masiva

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 22-12-2016
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
            ##Se instancia la produccion del insumo
            insumo_produccion = InsumoProduccion.objects.get(insumo__nombre_insumo=load_file[i,2],anho_registro=anho_registro)
            ## Se busca el proveedpr por el rif
            proveedor = Proveedor.objects.filter(rif=load_file[i,5])
            ## Si existe se instancia
            if(proveedor):
                proveedor = proveedor.get()
            ## De lo contrario se crea un nuevo objecto
            else:
                proveedor = Proveedor()
                proveedor.nombre = load_file[i,4]
                proveedor.rif = load_file[i,5]
                pais = Pais.objects.get(nombre_pais=load_file[i,3])
                proveedor.pais = pais
                ## Se prueba si el modelo es válido
                try:
                    proveedor.full_clean()
                    proveedor.save()
                except ValidationError as e:
                    error.append(e.message_dict)
            ## Se crea el modelo de insumo_producción
            insumo_proveedor = InsumoProveedor()
            insumo_proveedor.precio_compra_bs = load_file[i,6]
            insumo_proveedor.precio_compra_usd = load_file[i,7]
            insumo_proveedor.cantidad_comprada = load_file[i,8]
            insumo_proveedor.unidad_de_medida = load_file[i,9]
            insumo_proveedor.proveedor = proveedor
            insumo_proveedor.insumo_produccion = insumo_produccion
            ## Se prueba si el modelo es válido
            try:
                insumo_proveedor.full_clean()
                insumo_proveedor.save()
            except ValidationError as e:
                error.append((i,e.message_dict))
                
        ## Si no se registraron errores devuelve el mensaje de los errores
        if(len(error)==0):
            return {'validacion':True,'message':str(_("Se realizó la carga con éxito"))}
        ## En caso contrario retorna los errores
        return {'validacion':False,'message':error} 


