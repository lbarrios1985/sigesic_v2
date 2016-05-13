"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace sedes_admin.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo sedes_admin
# @author Ing. Hugo Ramirez (hramirez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import CreateView
from .forms import RegistroSedesForm
from .models import RegistroSedes



__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

# Create your views here.


class SedesCreate(CreateView):
    """!
    Clase que registra sedes administrativas en el sistema

    @author Ing. Hugo Ramirez (hramirez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 09-05-2016
    @version 2.0.0
    """
    model = RegistroSedes()
    form_class = RegistroSedesForm
    template_name = 'sedes-admin.registro.html'

    def get(self,request):
        form_name = RegistroSedesForm()
        return render_to_response('sedes-admin.registrar.html', {'form':form_name}, context_instance=RequestContext(request))
    def post(self,request):
        """!
        Metodo que valida el formulario de ser positivo registrar los datos
        de la sede administrativa

        @author Ing. Hugo Ramirez (hramirez at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 09-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de RegistroSedes
        @return Retorna el formulario validado
        """
        form = RegistroSedesForm(request.POST)


        if(form.is_valid()):

            self.model.nombre_sede = form.cleaned_data['nombre_sede']
            self.model.tipo_carretera = form.cleaned_data['tipo_carretera']
            self.model.nombre_carretera = form.cleaned_data['nombre_carretera']
            self.model.tipo_edificacion = form.cleaned_data['tipo_edificacion']
            self.model.nombre_edificacion = form.cleaned_data['nombre_edificacion']
            self.model.nombre_sector = form.cleaned_data['nombre_sector']
            self.model.tipo_tenencia = form.cleaned_data['tipo_tenencia']
            self.model.metros_cuadrados = form.cleaned_data['metros_cuadrados']
            self.model.metros_cuadrados_construccion = form.cleaned_data['metros_cuadrados_construccion']
            self.model.autonomia_electrica = form.cleaned_data['autonomia_electrica']
            self.model.consumo_electrico = form.cleaned_data['consumo_electrico']
            self.model.consumo_electrico = form.cleaned_data['consumo_agua']
            self.model.consumo_electrico = form.cleaned_data['consumo_gas']
            self.model.save()

        return render_to_response('sedes-admin.registrar.html', {'form':form}, context_instance=RequestContext(request))