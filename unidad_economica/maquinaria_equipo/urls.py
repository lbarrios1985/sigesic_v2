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
from .views import maquinariaView

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

urlpatterns = [
    url(r'^registro/', maquinariaView.as_view(), name='maquinaria_equipos'),
]
