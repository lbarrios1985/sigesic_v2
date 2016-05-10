"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidadeconomica.views
#
# Clases, atributos, métodos y/o funciones a implementar para las vistas del módulo unidadeconomica
# @author Eveli Ramírez (eramirez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 04-05-2016
# @version 2.0
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView

from .forms import UnidadEconomicaForm
from .models import UnidadEconomica

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


class UnidadEconomicaCreate(CreateView):
    """!
    Clase que registra los datos de la unidad económica

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 04-05-2016
    @version 2.0
    """
    template = "unidadeconomica.registro.html"

    def get(self, request):
        formulario = UnidadEconomicaForm()
        return render(request, self.template, {'ue': formulario})

    """
    def post(self, request):
        mensaje = "Datos guardados satisfactoriamente"
        formulario = unidadEconomicaForm()
        modeloue = unidad_economica()
        modeloue.rif = request.POST['rif']
        modeloue.nombre_ue = request.POST['nombre_ue']
        modeloue.razon_social = request.POST['razon_social']
        modeloue.nro_planta = request.POST['nro_planta']
        modeloue.nro_unid_comercializadora = request.POST['nro_unid_comercializadora']
        modeloue.servicio = request.POST['servicio']
        modeloue.orga_comunal = request.POST['orga_comunal']
        modeloue.casa_matriz_franquicia = request.POST['casa_matriz_franquicia']
        modeloue.nro_franquicias = request.POST['nro_franquicias']
        modeloue.save()
        return render(request, self.template, {'mensaje':mensaje})
    """
