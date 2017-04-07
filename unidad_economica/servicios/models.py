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
from django.core import signing
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
from base.models import CaevClase, Pais, AnhoRegistro, Cliente
from base.constant import MONEDAS, TIPO_SERVICIO, COLUMNS_CM

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

    ## Define los campos y validaciones necesarias para el archivo de carga masiva
    cm_fields = [
        {'field': 'id', 'title': str(_("Etiqueta")), 'max_length': 0, 'null': False},
        {'field': 'nombre_servicio', 'title': str(_("Nombre del Servicio")), 'max_length': 45, 'null': False},
        {'field': 'tipo_servicio', 'title': str(_("Tipo de Servicio")), 'max_length': 45, 'null': False},
        {'field': 'caev', 'title': str(_("Código")), 'max_length': 5, 'null': False},
        {'field': 'cantidad_clientes', 'title': str(_("Cantidad de Clientes")), 'max_length': 5, 'null': True}
    ]
    
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
        
        datos = []
        
        if not rel_id is None:
            ## Agrega los datos para la sub unidad solicitada
            for serv in Servicio.objects.filter(subunidad__id=rel_id):
                id = signing.dumps(serv.pk)
                datos.append([id, serv.nombre_servicio, serv.tipo_servicio, serv.caev.clase, serv.cantidad_clientes])

        return {'cabecera': self.cm_fields, 'datos': datos, 'output': 'servicios'}
    
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

        if len(load_file.row_range()) == 1:
            error.append(str(_("El archivo seleccionado esta vacio")))
        elif not [] == []:
            cabezera = [c['field'] for c in self.cm_fields]
            error.append(
                str(_("Verifique las cabeceras del archivo y la informacion a suministrar, "
                      "deben estar en el siguiente orden: %s" % str(cabezera)))
            )
        elif error:
            return {'validacion': False, 'message': error}


        valid = self.__validar_cm(load_file)

        if not valid['result']:
            return {'validacion': False, 'message': valid['errors']}

        for i in range(1,len(load_file.row_range())):

            ## Se intancia el caev
            caev = CaevClase.objects.get(clase=load_file[i,3])

            try:
                ## Se crea el registro para el servicio o se actualizan los datos en caso de existir
                Servicio.objects.update_or_create(pk=signing.loads(load_file[i, 0]), defaults={
                    'nombre_servicio': load_file[i, 1], 'tipo_servicio': load_file[i, 2],
                    'caev': caev, 'cantidad_clientes': load_file[i, 4], 'subunidad': subunidad
                })
            except ValidationError as e:
                error.append((i,e.message_dict))
            except Exception as e:
                error.append({i: e})

        ## Si no se registraron errores devuelve el mensaje de los errores
        if(len(error)==0):
            return {'validacion':True,'message':str(_("Se realizó la carga con éxito"))}
        ## En caso contrario retorna los errores
        return {'validacion':False,'message':error}

    def __validar_cm(self, archivo):

        errors = []
        validacion = {'result': True, 'errors': errors, 'cells': []}

        # Verifica que la cantidad de columnas sea la correcta
        if archivo.to_array()[0].__len__() != self.cm_fields.__len__():
            errors.append(str(_("El número de columnas no corresponde a los datos esperados")))
        if archivo.row[0] != [f['title'] for f in self.cm_fields]:
            errors.append(str(_("Las cabeceras del archivo no corresponde con las esperadas")))

        for i in range(1, len(archivo.row_range())):
            ## Evalúa si el código CAEV indicado en el archivo se encuentra registrado en el sistema
            try:
                CaevClase.objects.get(clase=archivo[i,3])
            except CaevClase.DoesNotExist:
                if archivo[i,3]:
                    errors.append("El campo %s contiene un Código Caev no válido" % (str(COLUMNS_CM[3]) + str(i+1)))

            for j in range(0, self.cm_fields.__len__()):
                ## Captura el campo del archivo a procesar. Ej. A1, A2, B1, B2, etc...
                campo_archivo = str(COLUMNS_CM[j]) + str(i+1)
                ## Captura el campo del modelo para sus respectivas validaciones
                campo_tabla = self._meta.get_field(self.cm_fields[j]['field'])

                ## Condición que evalúa si el campo permite valores vacios o nulos
                if (not campo_tabla.blank or not campo_tabla.null) and not archivo[i, j]:
                    errors.append("El campo %s no debe estar vacio" % campo_archivo)

                ## Condición que evalúa si el campo permite los valores indicados en el archivo
                if archivo[i, j] and campo_tabla.choices and not archivo[i, j] in [c[0] for c in campo_tabla.choices]:
                    errors.append("El campo %s contiene valores no permitidos. Los datos validos son: %s sin comillas" % (
                        campo_archivo, str([c[0] for c in campo_tabla.choices])
                    ))

                ## Condición que evalúa la longitud máxima permitida por el campo
                if campo_tabla.max_length and archivo[i, j].__len__() > campo_tabla.max_length:
                    errors.append(
                        "El campo %s debe contener máximo %s carácteres" % (
                            campo_archivo, self.cm_fields[j]['max_length']
                        )
                    )

                ## Condición que evalúa la restricción de campo único en la tabla
                if archivo[i, j] and campo_tabla.unique and self.objects.filter(**{self.cm_fields[j]['field']: archivo[i, j]}):
                    errors.append("El campo %s contiene un valor ya registrado en el sistema" % campo_archivo)
                try:
                    ## Condición que evalúa si los datos suministrados corresponden a un campo de tipo Integer
                    if campo_tabla.get_internal_type == 'IntegerField' and not archivo[i, j].isdigit():
                        errors.append("El campo %s debe ser un número entero" % campo_archivo)
                except Exception as e:
                    pass

        ## Si se enontraron errores la validación retorna falso con sus respectivos mensajes
        if errors:
            validacion['result'] = False
            validacion['errors'] = errors

        return validacion
    
        
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

    ## Define los campos y validaciones necesarias para el archivo de carga masiva
    cm_fields = [
        {'field': 'id', 'title': str(_("Etiqueta")), 'max_length': 0, 'null': False},
        {'field': 'servicio', 'title': str(_("Nombre del Servicio")), 'max_length': 45, 'null': False},
        {'field': 'pais', 'title': str(_("Ubicación")), 'max_length': 45, 'null': False},
        {'field': 'nombre', 'title': str(_("Nombre del Cliente")), 'max_length': 45, 'null': False},
        {'field': 'rif', 'title': str(_("R.I.F.")), 'max_length': 10, 'null': True},
        {'field': 'precio', 'title': str(_("Precio")), 'max_length': 3, 'decimal_places': 5, 'null': False},
        {'field': 'tipo_moneda', 'title': str(_("Tipo de Moneda")), 'max_length': 3, 'null': False},
        {
            'field': 'monto_facturado', 'title': str(_("Monto Facturado")), 'max_length': 20, 'decimal_places': 5,
            'null': False
        },
        {'field': 'servicio_prestado', 'title': str(_("# Servicios Prestados")), 'max_length': 20, 'null': False},
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
                        
        return {'cabecera': self.cm_fields, 'datos': datos, 'output': 'servicios_cliente'}
    
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