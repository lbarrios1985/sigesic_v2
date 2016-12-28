"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package maquinaria_equipos.urls
#
# Urls del módulo maquinaria_equipos
# @author Hugo Ramírez (hramirez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 09-06-2016
# @version 2.0
from __future__ import unicode_literals
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import maquinariaCreate, maquinaria_get_data

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

urlpatterns = [
    url(r'^registro', login_required(maquinariaCreate.as_view()), name='maquinaria_equipos_create'),
]

# Urls usadas para ajax
urlpatterns += [
    url(r'^ajax/maquinaria-data$', login_required(maquinaria_get_data) ,name="maquinaria_data"),
]
