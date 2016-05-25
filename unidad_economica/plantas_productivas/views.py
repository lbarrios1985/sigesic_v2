"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.plantas_prodcutivas.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo de plantas productivas
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy

from unidad_economica.sub_unidad_economica.models import (
    SubUnidadEconomica,SubUnidadEconomicaDirectorio, SubUnidadEconomicaCapacidad, SubUnidadEconomicaProceso,
    SubUnidadEconomicaPrincipalProceso,
    )
from base.models import Parroquia
from .forms import PlantasProductivasForm
from unidad_economica.directorio.models import Directorio
from base.constant import CREATE_MESSAGE, TIPO_SUB_UNIDAD
from base.classes import Seniat

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

# Create your views here.
class PlantasProductivasCreate(SuccessMessageMixin,CreateView):
    """!
    Clase que registra las plantas productivas

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 03-05-2016
    @version 2.0.0
    """
    model = SubUnidadEconomica
    form_class = PlantasProductivasForm
    template_name = "plantas.productivas.create.html"
    success_url = reverse_lazy('plantas_create')
    success_message = CREATE_MESSAGE
    
    def get_initial(self):
        """!
        Metodo que permite cargar datos en el formulario
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 09-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna los datos del rif
        """
        rif = self.request.user
        datos_iniciales = super(PlantasProductivasCreate, self).get_initial()
        datos_iniciales['rif'] = self.request.user.username

        datos_rif = Seniat()
        seniat = datos_rif.buscar_rif(rif)
        datos_iniciales['nombre_ue'] = datos_rif.nombre
        datos_iniciales['razon_social'] = datos_rif.nombre

        return datos_iniciales
    
    def get_context_data(self, **kwargs):
        kwargs['object_list'] = SubUnidadEconomicaProceso.objects.all()
        return super(PlantasProductivasCreate, self).get_context_data(**kwargs)

    def form_valid(self, form):
        """!
        Metodo que valida si el formulario es valido, en cuyo caso se procede a registrar los datos de la planta productiva
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 09-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        
        ## Se crea un diccionario de la data recibida por POST
        dictionary = dict(self.request.POST.lists())
        
        parroquia = Parroquia.objects.get(pk=self.request.POST['parroquia'])

        ## Se crea y se guarda el modelo de directorio
        directorio = Directorio()
        directorio.prefijo_uno=form.cleaned_data['prefijo_uno']
        directorio.direccion_uno=form.cleaned_data['direccion_uno']
        directorio.prefijo_dos=form.cleaned_data['prefijo_dos']
        directorio.direccion_dos=form.cleaned_data['direccion_dos']
        directorio.prefijo_tres=form.cleaned_data['prefijo_tres']
        directorio.direccion_tres=form.cleaned_data['direccion_tres']
        directorio.prefijo_cuatro=form.cleaned_data['prefijo_cuatro']
        directorio.direccion_cuatro=form.cleaned_data['direccion_cuatro']
        directorio.parroquia = parroquia
        #directorio.coordenadas = form.cleaned_data['coordenada']
        directorio.save()
        
        ## Se crea y se guarda el modelo de sub_unidad_economica
        self.object = form.save(commit=False)
        self.object.nombre_sub = form.cleaned_data['nombre_sub']
        self.object.rif = form.cleaned_data['rif']
        self.object.telefono = form.cleaned_data['telefono']
        self.object.tipo_sub_unidad = TIPO_SUB_UNIDAD[1][0]
        #modelSubUnidad.tipo_tenencia_id = form.cleaned_data['tipo_tenencia']
        self.object.m2_contruccion = form.cleaned_data['m2_contruccion']
        self.object.m2_terreno = form.cleaned_data['m2_terreno']
        self.object.autonomia_electrica = form.cleaned_data['autonomia_electrica']
        self.object.consumo_electrico = form.cleaned_data['consumo_electrico']
        self.object.cantidad_empleados = form.cleaned_data['cantidad_empleados']
        self.object.sede_servicio = int(form.cleaned_data['sede_servicio'])
        self.object.save()

         ## Se llama a la función que creará las actividades economicas
        self.modificar_diccionario(dictionary,self.object)
        
        ## Se crea y se guarda en el modelo del capacidad de la sub-unidad
        capacidad = SubUnidadEconomicaCapacidad()
        #proceso.codigo_ciiu = form.cleaned_data['codigo_ciiu_id']
        capacidad.capacidad_instalada_texto = form.cleaned_data['capacidad_instalada_texto']
        capacidad.capacidad_instalada_medida = form.cleaned_data['capacidad_instalada_medida']
        capacidad.capacidad_utilizada = form.cleaned_data['capacidad_utilizada']
        capacidad.sub_unidad_economica = self.object
        capacidad.save()
        
        
        ## Se crea y se guarda la tabla intermedio entre directorio-sub unidad
        directorio_subunidad = SubUnidadEconomicaDirectorio()
        directorio_subunidad.directorio = directorio
        directorio_subunidad.sub_unidad_economica = self.object
        directorio_subunidad.save()
        
        return super(PlantasProductivasCreate, self).form_valid(form)
    
    def modificar_diccionario(self, dictionary, model):
        """!
        Metodo que extrae los datos de la tabla de actividades economicas en un diccionario y las guarda en el modelo respectivo
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 09-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param dictionary <b>{object}</b> Objeto que contiene el diccionario a procesar
        @param model <b>{object}</b> Objeto que contiene el modelo al que se hace la referencia
        @return Retorna el formulario validado
        """
        for i in range(0,len(dictionary['nombre_proceso_tb'])):
            ## Se crea y se guarda en el modelo del proceso de la sub-unidad
            proceso = SubUnidadEconomicaProceso()
            proceso.tipo_proceso = dictionary['tipo_proceso_tb'][i]
            proceso.nombre_proceso = dictionary['nombre_proceso_tb'][i]
            proceso.descripcion_proceso = dictionary['descripcion_proceso_tb'][i]
            proceso.estado_proceso = int(dictionary['estado_proceso_tb'][i])
            proceso.save()
            
            ## Se crea y se guarda la tabla intermedio entre sub unidad y el proceso de la sub unidads
            sub_unidad_proceso = SubUnidadEconomicaPrincipalProceso()
            sub_unidad_proceso.sub_unidad_economica = model
            sub_unidad_proceso.sub_unidad_economica_proceso = proceso
            sub_unidad_proceso.save()
       