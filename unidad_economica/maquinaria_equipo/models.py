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

from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models import AnhoRegistro
from base.constant import ESTADO_ACTUAL_MAQUINARIA
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomicaProceso
# Create your models here.

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

    pais_origen = models.CharField(max_length=100)

    descripcion_maquinaria = models.CharField(max_length=200)

    years_fab = models.DateField()

    date = models.DateField(blank=False)

    vida_util = models.IntegerField()

    estado_actual = models.CharField(max_length=2)

    anho_registro = models.ForeignKey(AnhoRegistro)

    def __str__(self):
        return self.nombre_sub

    def carga_masiva_init(self, anho=None, rel_id=None):
        """!
        Método que establece los parámetros a mostrar con su rerspectiva información en los archivos de carga masiva

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 11-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param anho <b>anho</b> Condición que evalúa si extraer los datos del modelo para un año en partícular
        @param rel_id <b>rel_id</b> Entero que contiene el identificador del modelo asociado
        @return Devuelve los campos del archivo de carga masiva
        """

        ## Define los campos y validaciones necesarias para el archivo de carga masiva
        fields = [
            {
                'field': 'id',
                'title': str(_("Etiqueta")),
                'max_length': 0,
                'null': False,
                'type': 'string'
            },
            {
                'field': 'nombre_maquinaria',
                'title': str(_("Nombre de la Maquinaria")),
                'max_length': 100,
                'null': False,
                'type': 'string'
            },
            {
                'field': 'descripcion_maquinaria',
                'title': str(_("Descripción")),
                'max_length': 200,
                'null': False,
                'type': 'string'
            },
            {
                'field': 'pais_origen',
                'title': str(_("País de Fabricación")),
                'max_length': 100,
                'null': False,
                'type': 'string'
            },
            {
                'field': 'years_fab',
                'title': str(_("Año de Fabricación")),
                'max_length': 4,
                'null': False,
                'type': 'year'
            },
            {
                'field': 'date',
                'title': str(_("Año de Adquisición")),
                'max_length': 4,
                'null': True,
                'type': 'year'
            },
            {
                'field': 'vida_util',
                'title': str(_("Vida util")),
                'max_length': 2,
                'null': False,
                'type': 'integer'
            },
            {
                'field': 'estado_actual',
                'title': str(_("Estado Actual")),
                'max_length': 2,
                'null': False,
                'type': 'string'
            }
        ]

        datos = []

        if not anho is None and not rel_id is None:
            ## Agrega los datos para el año y sub unidad solicitada
            for maq in self.objects.filter(anho_registro__anho=anho, proceso_sub_unidad__pk=rel_id):
                estado_actual = ''
                for em in ESTADO_ACTUAL_MAQUINARIA:
                    if em[0] == maq.estado_actual:
                        estado_actual = str(em[1])

                datos.append([
                    maq.pk, maq.nombre_maquinaria, maq.descripcion_maquinaria, maq.pais_origen, maq.years_fab,
                    maq.date, maq.vida_util, estado_actual
                ])

        return {'cabecera': fields, 'datos': datos, 'output': 'maquinaria_equipo'}
