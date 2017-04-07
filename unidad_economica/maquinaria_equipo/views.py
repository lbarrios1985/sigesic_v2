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
from django.http import JsonResponse
from django.views.generic import CreateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from base.constant import CREATE_MESSAGE, ESTADO_ACTUAL_MAQUINARIA
from base.models import Pais
from .models import maquinariaModel
from .forms import MaquinariaForm
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica, SubUnidadEconomicaProceso

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"



class maquinariaCreate(SuccessMessageMixin,CreateView):
    """!
    Clase que permite el acceso
    @author Hugo Ramirez (hramirez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-06-2016
    """

    model = maquinariaModel
    form_class = MaquinariaForm
    template_name = 'maquinaria.equipo.base.html'
    success_url = reverse_lazy('maquinaria_equipos_create')
    success_message = CREATE_MESSAGE
    
    def get_form_kwargs(self):
        """!
        Metodo que permite guardar el username en los kwargs
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 14-07-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el kwargs con el username
        """
        kwargs = super(maquinariaCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """!
        Metodo que valida si el formulario es valido, en cuyo caso se procede a registrar los datos de la maquinaria
    
        @author Hugo Ramirez (hramirez at cenditel.gob.ve) / Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 08-06-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """

        ## Se instancia el proceso de la sub-unidad
        proceso_sub_unidad = SubUnidadEconomicaProceso.objects.get(pk=form.cleaned_data['nombre_proceso'])
        
        ## Se instancia el país
        pais = Pais.objects.get(pk=form.cleaned_data['pais_origen'])

        ## Se guarda el modelo de maquinaria
        self.object = form.save(commit=False)
        self.object.nombre_maquinaria = form.cleaned_data['nombre_maquinaria']
        self.object.descripcion_maquinaria = form.cleaned_data['descripcion_maquinaria']
        self.object.anho_fabricacion = form.cleaned_data['anho_fabricacion']
        self.object.anho_adquisicion = form.cleaned_data['anho_adquisicion']
        self.object.vida_util = form.cleaned_data['vida_util']
        self.object.estado_actual = form.cleaned_data['estado_actual']
        self.object.uso_energia = form.cleaned_data['uso_energia']
        self.object.proceso_sub_unidad = proceso_sub_unidad
        self.object.save()

        return super(maquinariaCreate, self).form_valid(form)
    
    
def maquinaria_get_data(request):
    """!
    Metodo que extrae los datos de la maquinaria relacionados con la sub-unidad

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 26-12-2016
    @param request <b>{object}</b> Recibe la peticion
    @return Retorna el json con las subunidades que consiguió
    """
    datos = {'data':[]}
    # Recibe por get el id de subunidad
    subid = request.GET.get('subunidad_id', None)
    if(subid):
        estado = dict(ESTADO_ACTUAL_MAQUINARIA)
        for maq in maquinariaModel.objects.filter(proceso_sub_unidad__sub_unidad_economica_id=subid).all():
            lista = []
            lista.append(maq.proceso_sub_unidad.sub_unidad_economica.nombre_sub)
            lista.append(maq.proceso_sub_unidad.nombre_proceso)
            lista.append(maq.nombre_maquinaria)
            lista.append(maq.pais_origen.nombre)
            lista.append(maq.descripcion_maquinaria)
            lista.append(maq.anho_fabricacion)
            lista.append(maq.vida_util)
            lista.append(maq.anho_adquisicion)
            lista.append(str(estado.get(maq.estado_actual)))
            datos['data'].append(lista)
        
        return JsonResponse(datos,safe=False)
    return JsonResponse("No se envío el id de la subunidad",safe=False)