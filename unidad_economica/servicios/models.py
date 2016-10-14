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
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
from base.models import CaevClase, Pais, AnhoRegistro, Cliente
from base.constant import MONEDAS

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
                'field': 'nombre_servicio',
                'title': str(_("Nombre del Servicio")),
                'max_length': 45,
                'null': False,
                'related':False,
                'depend':False,
                'type': 'string'
            },
            {
                'field': 'tipo_servicio',
                'title': str(_("Tipo de Servicio")),
                'max_length': 45,
                'null': False,
                'related':False,
                'depend':True,
                'related_app':'servicios',
                'related_model':'TipoServicio',
                'need_object':True,
                'filtro':'nombre',
                'type': 'string'
            },
            {
                'field': 'caev',
                'title': str(_("Código")),
                'max_length': 5,
                'null': False,
                'related':False,
                'depend':True,
                'related_app':'base',
                'related_model':'CaevClase',
                'type': 'string'
            },
            {
                'field': 'cantidad_clientes',
                'title': str(_("Cantidad de Clientes")),
                'max_length': 5,
                'null': True,
                'related':False,
                'depend':False,
                'type': 'string'
            },
        ]

        datos = []
        relation = {}
        
        if not anho is None and not rel_id is None:
            ## Agrega los datos para el año y sub unidad solicitada
            for serv in Servicio.objects.filter(anho_registro__anho=anho,subunidad__id=rel_id):
                datos.append([
                    '', serv.nombre_servicio, serv.tipo_servicio.nombre, serv.caev.clase,
                    serv.cantidad_clientes
                ])
                        
            relation = {
                'padre':{
                    'app':'sub_unidad_economica',
                    'mod':'SubUnidadEconomica',
                    'field':'subunidad',
                    'child':'Servicio',
                    'instance':SubUnidadEconomica.objects.get(pk=rel_id)
                },
            }

        return {'cabecera': fields, 'datos': datos, 'output': 'servicios', 'relation':relation}
    
        
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
    tipo_moneda = models.CharField(max_length=3)
    
    ## Monto facturado del servicio
    monto_facturado = models.DecimalField(max_digits=20,decimal_places=5)
    
    ## Establece la relación con el país
    pais = models.ForeignKey(Pais)
    
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
                'related':True,
                'depend':False,
                'related_model':'Servicio',
                'type': 'string'
            },
            {
                'field': 'servicio',
                'title': str(_("Nombre del Servicio")),
                'max_length': 45,
                'null': False,
                'related':False,
                'depend':True,
                'related_app':'servicios',
                'related_model':'Servicio',
                'need_object':True,
                'filtro':'nombre_servicio',
                'type': 'string'
            },
            {
                'field': 'pais',
                'title': str(_("Ubicación")),
                'max_length': 45,
                'null': False,
                'related':False,
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
                'related':False,
                'depend':False,
                'type': 'string'
            },
            {
                'field': 'rif',
                'title': str(_("Rif")),
                'max_length': 10,
                'null': True,
                'related':False,
                'depend':False,
                'type': 'string'
            },
            {
                'field': 'precio',
                'title': str(_("Precio")),
                'max_length': 3,
                'decimal_places':5,
                'null': False,
                'related':False,
                'depend':False,
                'type': 'double'
            },
            {
                'field': 'tipo_moneda',
                'title': str(_("Tipo de Moneda")),
                'max_length': 3,
                'null': False,
                'related':False,
                'depend':False,
                'type': 'string'
            },
            {
                'field': 'monto_facturado',
                'title': str(_("Monto Facturado")),
                'max_length': 20,
                'decimal_places':5,
                'null': False,
                'related':False,
                'depend':False,
                'type': 'double'
            },
            {
                'field': 'servicio_prestado',
                'title': str(_("# Servicios Prestados")),
                'max_length': 20,
                'null': False,
                'related':False,
                'depend':False,
                'type': 'integer'
            },
        ]

        datos = []
        relation = {}

        if not anho is None and not rel_id is None:
            ## Agrega los datos para el año y sub unidad solicitada
            dic_um = dict(MONEDAS)
            for serv in Servicio.objects.filter(subunidad__id=rel_id):
                serv_cli = ServicioCliente.objects.filter(servicio=serv.pk)
                for item in range(serv.cantidad_clientes):
                    #codigo = str(fact.producto_id)+" "+str(fact.pk)
                    if serv_cli:
                        unidad_medida = str(dic_um.get(fact.unidad_de_medida))
                        """datos.append([
                            '', prod.producto.nombre_producto, prod.producto.especificacion_tecnica, prod.producto.marca,
                            prod.producto.caev.pk,prod.cantidad_clientes, prod.cantidad_insumos, prod.cantidad_insumos,
                            prod.cantidad_produccion, unidad_medida
                        ])"""
                    else:
                        datos.append([
                            '', serv.nombre_servicio, '' ,'', '', '', '','','',''
                        ])
                        
            relation = {
                'padre':{
                    'app':'sub_unidad_economica',
                    'mod':'SubUnidadEconomica',
                    'field':'subunidad',
                    'child':'Servicio',
                    'instance':SubUnidadEconomica.objects.get(pk=rel_id)
                },
            }
        return {'cabecera': fields, 'datos': datos, 'output': 'servicios_cliente', 'relation':relation}