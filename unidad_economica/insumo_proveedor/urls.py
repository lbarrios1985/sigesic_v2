"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package insumo_proveedor.urls
#
# Urls del módulo maquinaria_equipos
# @author Hugo Ramírez (hramirez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 14-09-2016
# @version 2.0
from __future__ import unicode_literals
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


urlpatterns = [
    url(r'^registro$', login_required(InsumoCreate.as_view()) ,name="insumo_create"),
    url(r'^registro_proveedor$', login_required(InsumoProveedorCreate.as_view()) ,name="proveedor_create"),
]

# Urls usadas para ajax
urlpatterns += [
    url(r'^ajax/insumo-data$', login_required(insumo_get_data) ,name="insumo_data"),
    url(r'^ajax/clientes-data$', login_required(proveedor_get_data) ,name="proveedor_data"),
]
