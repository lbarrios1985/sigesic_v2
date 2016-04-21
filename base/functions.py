"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace base.functions
#
# Contiene las funcionas básicas de la aplicación
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


def verificar_rif(nrorif):
    """!
    Función que permite verificar si el dígito que valida el RIF es el correcto

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 21-04-2016
    @param nrorif Cadena de texto que contiene el numero de R.I.F. a verificar
    @return Devuelve Falso si el numero de R.I.F. es incorrecto, en caso contrario devuelve Verdadero
    """

    if not nrorif or nrorif.__len__()<10:
        return False
    elif nrorif.__len__() == 10:
        suma = 0
        divisor = 11
        resto = 0
        digito = 0
        tiporif = 0
        digitoValidado = 0

        if nrorif[0:1]=="V" or nrorif[0:1]=="E" or nrorif[0:1]=="J" or nrorif[0:1]=="P" or nrorif[0:1]=="G":
            if nrorif[0:1]=="V":
                tiporif = 1
            elif nrorif[0:1]=="E":
                tiporif = 2
            elif nrorif[0:1]=="J":
                tiporif = 3
            elif nrorif[0:1]=="P":
                tiporif = 4
            elif nrorif[0:1]=="G":
                tiporif = 5

            suma = ((tiporif*4) + (int(nrorif[1:2])*3) + (int(nrorif[2:3])*2)
                    + (int(nrorif[3:4])*7) + (int(nrorif[4:5])*6) + (int(nrorif[5:6])*5)
                    + (int(nrorif[6:7])*4) + (int(nrorif[7:8])*3) + (int(nrorif[8:9])*2))

            resto = suma%divisor

            digitoValidado = divisor - resto

        if int(digitoValidado)>=10:
            digitoValidado=0

        if int(nrorif[9:10])==int(digitoValidado):
            return True
        else:
            return False