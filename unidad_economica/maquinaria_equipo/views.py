"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace maquinaria_equipos .views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo de maquinaria
# @author Hugo Ramirez (hramirez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 09-06-2016
# @version 2.0

from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from base.constant import CREATE_MESSAGE
from .models import maquinariaModel
from .forms import MaquinariaForm
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica, SubUnidadEconomicaProceso, SubUnidadEconomicaProceso

# Create your views here.

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"



class maquinariaView(CreateView):

    """!
    Clase que permite el acceso
    @author Hramirez (hramirez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-06-2016
    """

    model = maquinariaModel
    form_class = MaquinariaForm
    template_name = 'maquinaria.equipo.base.html'
    success_url = reverse_lazy('equipos')
    success_message = CREATE_MESSAGE

    def form_valid(self, form):

        #nombre_proceso = .objects.get(pk=self.request.POST['parroquia'])

        #self.object.nombre_proceso = SubUnidadEconomica.objects.get(pk=self.request.POST['id'])

        self.object = form.save(commit=False)
        self.object.nombre_maquinaria = form.cleaned_data['nombre_maquinaria']
        self.object.pais_origen = form.cleaned_data['pais_origen']
        self.object.descripcion_maquinaria = form.cleaned_data['descripcion_maquinaria']
        self.object.año_fabricacion = form.cleaned_data['año_fabricacion ']
        self.object.save()

        return super(maquinariaView, self).form_valid(form)

    def get_initial(self):

        datos = super(maquinariaView, self).get_initial()
        #datos["nombre_p"] = SubUnidadEconomicaProceso.objects.get(pk=1)
        #print(datos["nombre_p"].sub_unidad_economica_proceso.nombre_proceso)
        return datos