"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidadeconomica.utils
#
# Clases, atributos, métodos y/o funciones a implementar utilidades del módulo unidadeconomica
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 26-10-2016
# @version 2.0
from django.apps import apps
from django.utils.translation import ugettext_lazy as _
from base.functions import cargar_anho
from .models import CertificadoRegistro

def anho_pendiente(rif):
    """!
    Método para obtener el año pendiente de un usuario cuyo rif corresponda
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 26-10-2016
    @param rif <b>{string}</b> Recibe el rif del usuario que se desea validar
    @return Retorna los años pendientes por registrar
    """
    resultados = []
    certificado = CertificadoRegistro.objects.filter(ue__rif=rif)
    anho = cargar_anho()
    if(certificado):
        for item,key in anho:
            validar = True
            for cert in certificado.all():
                if(key==cert.anho_registro.aho):
                    validar = False
            if(validar):
                resultados.append((item,key))
        return [('',_('Seleccione..'))]+resultados
    return anho

def validar_anho(app,mod,**filtro):
    """!
    Método para validar el año de registro de un rif de usuario
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 26-10-2016
    @param app <b>{string}</b> Recibe el nombre de la aplicacion
    @param mod <b>{string}</b> Recibe el nombre del modelo de la aplicacion
    @param filtro <b>{dict}</b> Recibe el filtros y valores que se utilizarán
    @return Retorna el año de registro si existe
    """
    mensaje = {}
    modelo = apps.get_model(app, mod)
    model = modelo.objects.filter(**filtro)
    print(modelo)
    if(model):
        model = model.first()
        mensaje['validacion'] = True
        mensaje['anho_registro'] = model.anho_registro
    else:
        mensaje['validacion'] = False
    return mensaje
