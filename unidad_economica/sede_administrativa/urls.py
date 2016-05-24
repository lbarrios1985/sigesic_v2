"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace sedes_administrativa.urls
#
# Contiene las urls del módulo sedes_administrativa
# @author Ing. Hugo Ramirez (hramirez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
from django.conf.urls import url, patterns
from .views import SedesCreate

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

<<<<<<< HEAD
urlpatterns = patterns('', url(r'^registro$',SedesCreate.as_view(), name='sede_administrativa'),

=======
urlpatterns = patterns('',
    url(r'^registro$',SedesCreate.as_view(), name='sede_administrativa'),
>>>>>>> 9534f2ddf4ada0c0bb9ee91e2c4c22d081bce6f4
)
