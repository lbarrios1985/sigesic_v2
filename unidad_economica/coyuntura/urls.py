"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidad_economica.coyuntura.urls
#
# Urls del módulo coyuntura
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 09-01-2017
# @version 2.0

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import ProduccionCreate, produccion_get_data, ClientesCreate, clientes_get_data

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

urlpatterns = [
    url(r'^registro$', login_required(ProduccionCreate.as_view()), name='coyuntura_registro_create'),
    url(r'^registro_cliente$', login_required(ClientesCreate.as_view()) ,name="clientes_registro_create"),
]

# Urls usadas para ajax
urlpatterns += [
    url(r'^ajax/coyuntura-produccion-data$', login_required(produccion_get_data) ,name="coyuntura_produccion_data"),
    url(r'^ajax/coyuntura-clientes-data$', login_required(clientes_get_data) ,name="coyuntura_clientes_data"),
]
