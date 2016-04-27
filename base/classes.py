"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace base.classes
#
# Contiene las clases, atributos y métodos de uso común en el sistema
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

import logging

from urllib.request import urlopen
from xml.dom.minidom import parseString

logger = logging.getLogger('base')

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


class Seniat:
    """!
    Clase que permite consultar datos en el SENIAT

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 27-04-2016
    @version 2.0.0
    """

    def __init__(self):
        """!
        Método que inicializa la clase Seniat

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 27-04-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        """

        ## Número de RIF consultado
        self.rif = ''

        ## Nombre de la Persona asociada al número de RIF
        self.nombre = ''

        ## Indica si la persona es o no agente de retención de IVA
        self.agente_retencion_iva = ''

        ## Indica si la persona es o no contribuyente de IVA
        self.contribuyente_iva = ''

    def buscar_rif(self, rif=None):
        """!
        Método que ejecuta la búsqueda de datos de un número de RIF a consultar

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 27-04-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param rif <b>{string}</b> Número de RIF a consultar. El valor por defecto es Ninguno
        @return Devuelve la función privada de búsqueda de datos del RIF solicitado
        """
        if rif:
            return self.__buscar(rif)

    def __buscar(self, rif):
        """!
        Método privado que ejecuta la consulta de datos del RIF solicitado ante el SENIAT

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 27-04-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param rif <b>{string}</b> Número de RIF a consultar
        @return Devuelve Verdadero en caso de encontrar datos registrados en el SENIAT con el número de RIF solicitado,
                en caso contrario o al encontrar algún error de conexión, devuelve Falso
        """
        try:
            s = urlopen("http://contribuyente.seniat.gob.ve/getContribuyente/getrif?rif=%s" % rif, timeout=80)
            xml_data = s.read()
            dom = parseString(xml_data)
            self.rif = rif
            self.nombre = dom.childNodes[0].childNodes[0].firstChild.data
            self.agente_retencion_iva = dom.childNodes[0].childNodes[1].firstChild.data
            self.contribuyente_iva = dom.childNodes[0].childNodes[2].firstChild.data
            return True
        except Exception as e:
            self.rif = ''
            self.nombre = ''
            self.agente_retencion_iva = ''
            self.contribuyente_iva = ''

            logger.warning("Error al obtener información del RIF [%s]. Detalles: %s" % (rif, e))

            return False