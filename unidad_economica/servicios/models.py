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
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
from base.models import CaevClase, Pais, AnhoRegistro, Cliente
from base.constant import MONEDAS, TIPO_SERVICIO
import pyexcel

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
    
    ## Tipo de Servicio
    tipo_servicio = models.CharField(max_length=2,choices=TIPO_SERVICIO)
    
    ## Establece la relación con el código CAEV
    caev = models.ForeignKey(CaevClase)
    
    ## Cantidad de clientes
    cantidad_clientes = models.IntegerField()
    
    ## Establece la relación con la sub unidad económica
    subunidad = models.ForeignKey(SubUnidadEconomica)
    
    def carga_masiva_init(self, anho=None, rel_id=None):
        """!
        Método que establece los parámetros a mostrar con su rerspectiva información en los archivos de carga masiva

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 11-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
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
            },
            {
                'field': 'nombre_servicio',
                'title': str(_("Nombre del Servicio")),
                'max_length': 45,
                'null': False,
            },
            {
                'field': 'tipo_servicio',
                'title': str(_("Tipo de Servicio")),
                'max_length': 45,
                'null': False,
            },
            {
                'field': 'caev',
                'title': str(_("Código")),
                'max_length': 5,
                'null': False,
            },
            {
                'field': 'cantidad_clientes',
                'title': str(_("Cantidad de Clientes")),
                'max_length': 5,
                'null': True,
            },
        ]

        datos = []
        
        if not rel_id is None:
            ## Agrega los datos para la sub unidad solicitada
            for serv in Servicio.objects.filter(subunidad__id=rel_id):
                datos.append([
                    '', serv.nombre_servicio, serv.tipo_servicio, serv.caev.clase,
                    serv.cantidad_clientes
                ])

        return {'cabecera': fields, 'datos': datos, 'output': 'servicios'}
    
    def carga_masiva_load(self,path=None, anho=None, rel_id=None):
        """!
        Método para realizar la carga masiva

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 19-12-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param path <b>path</b> Recibe la ruta del archivo para abrir
        @param anho <b>anho</b> Condición que evalúa si extraer los datos del modelo para un año en partícular
        @param rel_id <b>rel_id</b> Tiene el id de la relación del padre
        @return Devuelve el mensaje
        """
        
        load_file = pyexcel.get_sheet(file_name=path)
        ## Se instancia la subunidad
        subunidad = SubUnidadEconomica.objects.get(pk=rel_id)
        ## Se define un arreglo para los errores
        error = []
        for i in range(1,len(load_file.row_range())):
            ## Se intancia el caev
            caev = CaevClase.objects.get(pk=load_file[i,3])
            ## Se crea el servicio
            servicio = Servicio()
            servicio.nombre_servicio = load_file[i,1]
            servicio.tipo_servicio = load_file[i,2]
            servicio.caev = caev
            servicio.cantidad_clientes = load_file[i,4]
            servicio.subunidad = subunidad
            try:
                servicio.full_clean()
                servicio.save()
            except ValidationError as e:
                error.append((i,e.message_dict))
        ## Si no se registraron errores devuelve el mensaje de los errores
        if(len(error)==0):
            return {'validacion':True,'message':str(_("Se realizó la carga con éxito"))}
        ## En caso contrario retorna los errores
        return {'validacion':False,'message':error} 
    
        
class ServicioCliente(models.Model):
    """!
    Clase que gestiona los datos para el registro de los Clientes en los Servicios

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-08-2016
    @version 2.0
    """
    
    ## Establece la relación con los datos del cliente
    cliente = models.ForeignKey(Cliente)
    
    ## Año de registro de la producción
    anho_registro = models.ForeignKey(AnhoRegistro)
    
    ## Número de servicios prestados por año
    servicio_prestado = models.IntegerField()
    
    ## Precio del servicio
    precio = models.DecimalField(max_digits=20,decimal_places=5)
    
    ## Tipo de moneda
    tipo_moneda = models.CharField(max_length=3,choices=MONEDAS)
    
    ## Monto facturado del servicio
    monto_facturado = models.DecimalField(max_digits=20,decimal_places=5)
    
    ## Establece la relación con la producción
    servicio = models.ForeignKey(Servicio)
    
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
            },
            {
                'field': 'servicio',
                'title': str(_("Nombre del Servicio")),
                'max_length': 45,
                'null': False,
            },
            {
                'field': 'pais',
                'title': str(_("Ubicación")),
                'max_length': 45,
                'null': False,
            },
            {
                'field': 'nombre',
                'title': str(_("Nombre del Cliente")),
                'max_length': 45,
                'null': False,
            },
            {
                'field': 'rif',
                'title': str(_("Rif")),
                'max_length': 10,
                'null': True,
            },
            {
                'field': 'precio',
                'title': str(_("Precio")),
                'max_length': 3,
                'decimal_places':5,
                'null': False,
            },
            {
                'field': 'tipo_moneda',
                'title': str(_("Tipo de Moneda")),
                'max_length': 3,
                'null': False,
            },
            {
                'field': 'monto_facturado',
                'title': str(_("Monto Facturado")),
                'max_length': 20,
                'decimal_places':5,
                'null': False,
            },
            {
                'field': 'servicio_prestado',
                'title': str(_("# Servicios Prestados")),
                'max_length': 20,
                'null': False,
            },
        ]

        datos = []

        if not anho is None and not rel_id is None:
            ## Agrega los datos para el año y sub unidad solicitada
            for serv in Servicio.objects.filter(subunidad__id=rel_id):
                serv_cli = ServicioCliente.objects.filter(servicio=serv.pk).all()
                if not serv_cli:
                    for item in range(serv.cantidad_clientes):
                        datos.append([
                            '', serv.nombre_servicio, '' ,'', '', '', '','',''
                        ])
                ## Si los hay igual cantidades de registros con lo que se marcó inicialmente
                ## se llena normalmente
                elif(len(serv_cli)==serv.cantidad_clientes):
                    for item in serv_cli:
                        datos.append([
                            '', serv.nombre_servicio, item.cliente.pais.nombre, item.cliente.nombre,
                            item.cliente.rif,item.precio, item.tipo_moneda, item.monto_facturado,
                            item.servicio_prestado
                        ])
                ## Si la cantidad de registros es distinta a lo que se marcó inicialmente
                ## se llena con los registros que existan, y se llena con campos vacios lo faltante
                elif(len(serv_cli)!=serv.cantidad_clientes):
                    for item in serv_cli:
                        datos.append([
                            '', serv.nombre_servicio, item.cliente.pais.nombre, item.cliente.nombre,
                            item.cliente.rif,item.precio, item.tipo_moneda, item.monto_facturado,
                            item.servicio_prestado
                        ])
                    for item in range(serv.cantidad_clientes-len(serv_cli)):
                        datos.append([
                            '', serv.nombre_servicio, '' ,'', '', '', '','',''
                        ])
                        
        return {'cabecera': fields, 'datos': datos, 'output': 'servicios_cliente'}
    
    def carga_masiva_load(self,path=None, anho=None, rel_id=None):
        """!
        Método para realizar la carga masiva

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 20-12-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param path <b>path</b> Recibe la ruta del archivo para abrir
        @param anho <b>anho</b> Condición que evalúa si extraer los datos del modelo para un año en partícular
        @param rel_id <b>rel_id</b> Tiene el id de la relación del padre
        @return Devuelve el mensaje
        """
        
        load_file = pyexcel.get_sheet(file_name=path)
        ## Se instancia la subunidad
        subunidad = SubUnidadEconomica.objects.get(pk=rel_id)
        ## Se intancia el año de registro
        anho_registro = AnhoRegistro.objects.filter(anho=anho).get()
        ## Se define un arreglo para los errores
        error = []
        for i in range(1,len(load_file.row_range())):
            ## Se busca el servicio
            servicio = Servicio.objects.filter(subunidad_id=rel_id,nombre_servicio=load_file[i,1]).get()
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
            ## Se crea el servicio del cliente
            servicio_cliente = ServicioCliente()
            servicio_cliente.precio = load_file[i,5]
            servicio_cliente.tipo_moneda = load_file[i,6]
            servicio_cliente.monto_facturado = load_file[i,7]
            servicio_cliente.servicio_prestado = load_file[i,8]
            servicio_cliente.anho_registro = anho_registro
            servicio_cliente.cliente = cliente
            servicio_cliente.servicio = servicio
            try:
                servicio_cliente.full_clean()
                servicio_cliente.save()
            except ValidationError as e:
                error.append((i,e.message_dict))
        ## Si no se registraron errores devuelve el mensaje de los errores
        if(len(error)==0):
            return {'validacion':True,'message':str(_("Se realizó la carga con éxito"))}
        ## En caso contrario retorna los errores
        return {'validacion':False,'message':error} 