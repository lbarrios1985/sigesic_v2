"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace base.urls
#
# Contiene las urls del módulo base
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
from django.conf.urls import url, patterns

from .ajax import get_data_rif, validar_rif_seniat, actualizar_combo, eliminar_registro, cargar_combo, anho_registro, client_data

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


urlpatterns = [
    url(r'^inicio/$', 'base.views.inicio', name='inicio'),
    url(r'^contacto/$', 'base.views.contacto', name='contacto'),
]


## URLs de peticiones AJAX
urlpatterns += [
    url(r'^ajax/get-data-rif/?$', get_data_rif, name='get_data_rif'),
    url(r'^ajax/validar-rif-seniat/?$', validar_rif_seniat, name='validar_rif_seniat'),
    url(r'^ajax/actualizar-combo/?$', actualizar_combo, name='actualizar_combo'),
    url(r'^ajax/eliminar-registro/$', eliminar_registro, name="eliminar_registro"),
    url(r'^ajax/cargar-combo/?$', cargar_combo, name='cargar_combo'),
    url(r'^ajax/anho-registro/$', anho_registro, name='anho_registro'),
    url(r'^ajax/cliente-data$', client_data ,name="ajax_cliente_data"),
]