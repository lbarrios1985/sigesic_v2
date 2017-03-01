"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace maquinaria_equipos .models
#
# Models del módulo maquinaria_equipos
# @author Hugo Ramirez (hramirez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 09-06-2016
# @version 2.0
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models import AnhoRegistro, Pais
from base.constant import ESTADO_ACTUAL_MAQUINARIA
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomicaProceso
import pyexcel

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

class maquinariaModel(models.Model):

    """!
    @author Hugo Ramirez (hramirez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-06-2016
    @version 2.0.0
    """

    proceso_sub_unidad = models.ForeignKey(SubUnidadEconomicaProceso)

    nombre_maquinaria = models.CharField(max_length=100)

    pais_origen = models.ForeignKey(Pais)

    descripcion_maquinaria = models.CharField(max_length=200)

    anho_fabricacion = models.IntegerField()

    anho_adquisicion = models.IntegerField()

    vida_util = models.IntegerField()

    estado_actual = models.CharField(max_length=2,choices=ESTADO_ACTUAL_MAQUINARIA)

    ## Define los campos y validaciones necesarias para el archivo de carga masiva
    cm_fields = [
        {'field': 'id', 'title': str(_("Etiqueta")), 'max_length': 0, 'null': False},
        {'field': 'nombre_maquinaria', 'title': str(_("Nombre de la Maquinaria")), 'max_length': 100, 'null': False},
        {'field': 'descripcion_maquinaria', 'title': str(_("Descripción")), 'max_length': 200, 'null': False},
        {'field': 'pais_origen', 'title': str(_("País de Fabricación")), 'max_length': 100, 'null': False},
        {'field': 'anho_fabricacion', 'title': str(_("Año de Fabricación")), 'max_length': 4, 'null': False},
        {'field': 'anho_adquisicion', 'title': str(_("Año de Adquisición")), 'max_length': 4, 'null': True},
        {'field': 'vida_util', 'title': str(_("Vida util")), 'max_length': 2, 'null': False},
        {'field': 'estado_actual', 'title': str(_("Estado Actual")), 'max_length': 2, 'null': False}
    ]

    def __str__(self):
        return self.nombre_maquinaria

    def carga_masiva_init(self, anho=None, rel_id= None):
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
        relation = {}
        
        if not rel_id is None:
            ## Agrega los datos para el año y sub unidad solicitada
            for maq in maquinariaModel.objects.filter(proceso_sub_unidad_id=rel_id):

                datos.append([
                    maq.pk, maq.nombre_maquinaria, maq.descripcion_maquinaria, maq.pais_origen.nombre, maq.anho_fabricacion,
                    maq.anho_adquisicion, maq.vida_util, maq.estado_actual
                ])
        return {'cabecera': self.cm_fields, 'datos': datos, 'output': 'maquinaria_equipo'}
    
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
        ## Se instancia el proceso de la sub-unidad
        proceso_sub_unidad = SubUnidadEconomicaProceso.objects.get(pk=rel_id)
        ## Se define un arreglo para los errores
        error = []
        for i in range(1,len(load_file.row_range())):
            ## Se instancia el país
            pais = Pais.objects.get(nombre=load_file[i,3])
            ## Se crea el modelo de maquinaria
            maquinaria = maquinariaModel()
            maquinaria.nombre_maquinaria = load_file[i,1]
            maquinaria.descripcion_maquinaria = load_file[i,2]
            maquinaria.pais_origen = pais
            maquinaria.anho_fabricacion = load_file[i,4]
            maquinaria.anho_adquisicion = load_file[i,5]
            maquinaria.vida_util = load_file[i,6]
            maquinaria.estado_actual = load_file[i,7]
            maquinaria.proceso_sub_unidad = proceso_sub_unidad
            ## Se prueba si el modelo es válido
            try:
                maquinaria.full_clean()
                maquinaria.save()
            except ValidationError as e:
                error.append((i,e.message_dict))
        
        ## Si no se registraron errores devuelve el mensaje de los errores
        if(len(error)==0):
            return {'validacion':True,'message':str(_("Se realizó la carga con éxito"))}
        ## En caso contrario retorna los errores
        return {'validacion':False,'message':error} 
