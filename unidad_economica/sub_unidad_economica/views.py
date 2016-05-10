"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.sub_unidad_economica.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo de sub unidades economicas
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import PlantasProductivasForm
from .models import SubUnidadEconomica
#from unidad_economica.directorio.models import DirectorioModel
from unidad_economica.directorio.forms import DirectorioForm
from base.constant import REGISTRO_MESSAGE

# Create your views here.
class PlantasCreate(SuccessMessageMixin,CreateView):
    """!
    Clase que registra las plantas productivas

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 03-05-2016
    @version 2.0.0
    """
    template_name = "subunidad_form.html"
    success_message = REGISTRO_MESSAGE
    cantidad_plantas = 2
    
    def get(self,request):
        """!
        Metodo para cargar el formulario cuando se hace un petición por GET

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 03-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @return Retorna los dos formularios (PlantasProductivasForm y DirectorioForm) vacios
        """
        form = PlantasProductivasForm
        directorio = DirectorioForm
        return render(request,self.template_name, {'form': form,'directorio':directorio,'cant':range(self.cantidad_plantas)})
    
    def post(self,request):
        """!
        Metodo para cargar el formulario cuando se hace un petición por POST

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 09-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @return Retorna los dos formularios (PlantasProductivasForm y DirectorioForm) con validaciones y errores
        """
        form = PlantasProductivasForm(request.POST)
        directorio = DirectorioForm(request.POST)
        #modelDirectorio = DirectorioModel
        modelSubUnidad = SubUnidadEconomica
        
        ## Se pasan los datos del formulario al modelo sub unidad económica
        if(form.is_valid()):
            modelSubUnidad.nombre_sub = form.cleaned_data['nombre_sub']
            #modelSubUnidad.tipo_coordenada = form.cleaned_data['tipo_coordenada']
            modelSubUnidad.coordenada_geografica = form.cleaned_data['coordenada_geografica']
            modelSubUnidad.telefono_planta = form.cleaned_data['telefono_planta']
            #modelSubUnidad.tipo_tenencia_id = form.cleaned_data['tipo_tenencia']
            modelSubUnidad.m2_contruccion = form.cleaned_data['m2_contruccion']
            modelSubUnidad.m2_terreno = form.cleaned_data['m2_terreno']
            modelSubUnidad.autonomia_electrica = form.cleaned_data['autonomia_electrica']
            modelSubUnidad.consumo_electrico = form.cleaned_data['consumo_electrico']
            #modelSubUnidad.codigo_ciiu_id = form.cleaned_data['codigo_ciiu_id']
            modelSubUnidad.capacidad_instalada_texto = form.cleaned_data['capacidad_instalada_texto']
            modelSubUnidad.capacidad_instalada_select = form.cleaned_data['capacidad_instalada_select']
            modelSubUnidad.capacidad_utilizada = form.cleaned_data['capacidad_utilizada']
            modelSubUnidad.sede_servicio = form.cleaned_data['sede_servicio']
            print(modelSubUnidad.nombre_sub)
            
        #print(form)
        #print(directorio)
        return render(request,self.template_name, {'form': form,'directorio':directorio,'cant':range(self.cantidad_plantas)})