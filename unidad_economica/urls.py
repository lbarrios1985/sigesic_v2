"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidad_economica.urls
#
# Urls del módulo unidad_economica
# @author Eveli Ramírez (eramirez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 04-05-2016
# @version 2.0
from __future__ import unicode_literals
from django.conf.urls import url, include
from .views import UnidadEconomicaCreate

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

urlpatterns = [
    url(r'^informacion-general/registro/', UnidadEconomicaCreate.as_view(), name="registro_ue"),
    url(r'^registro-mercantil/', include('unidad_economica.informacion_mercantil.urls')),
    url(r'^plantas-productivas/', include('unidad_economica.plantas_productivas.urls')),
    url(r'^sede-administrativa/', include('unidad_economica.sede_administrativa.urls')),
    url(r'^unidades-comercializadoras/', include('unidad_economica.unidades_comercializadoras.urls')),
    url(r'^', include('unidad_economica.sedes_admin.urls'))
]
