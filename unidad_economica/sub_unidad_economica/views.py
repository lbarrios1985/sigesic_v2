"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.sub_unidad_economica.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo de sub unidad económica
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.core import serializers

from .models import (
    SubUnidadEconomica,SubUnidadEconomicaDirectorio, SubUnidadEconomicaCapacidad, SubUnidadEconomicaProceso,
    SubUnidadEconomicaActividad
    )
from base.models import Parroquia, CaevRama
from .forms import SubUnidadEconomicaForm
from unidad_economica.directorio.models import Directorio
from unidad_economica.models import UnidadEconomica
from django.contrib.auth.models import User
from base.constant import CREATE_MESSAGE, TIPO_SUB_UNIDAD, TIPO_TENENCIA
from base.classes import Seniat

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

# Create your views here.
class SubUnidadEconomicaCreate(SuccessMessageMixin,CreateView):
    """!
    Clase que registra la sub unidad económica

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 03-05-2016
    @version 2.0.0
    """
    model = SubUnidadEconomica
    form_class = SubUnidadEconomicaForm
    template_name = "sub.unidad.economica.base.html"
    success_url = reverse_lazy('sub_unidad_create')
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
        datos_iniciales = super(SubUnidadEconomicaCreate, self).get_initial()
        datos_iniciales['rif'] = self.request.user.username

        datos_rif = Seniat()
        seniat = datos_rif.buscar_rif(rif)
        datos_iniciales['nombre_ue'] = datos_rif.nombre
        datos_iniciales['razon_social'] = datos_rif.nombre

        return datos_iniciales
    
    def get_context_data(self, **kwargs):
        """!
        Metodo que permite cargar nuevos valores en los datos de contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 09-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        
        buttons = '<a class="update_item" style="cursor: pointer"><i class="glyphicon glyphicon-pencil"></i></a>';
        buttons += '<a class="remove_item" style="cursor: pointer"><i class="glyphicon glyphicon-remove"></i></a>';
        if 'tipo_proceso_tb' in self.request.POST:
            dictionary = dict(self.request.POST.lists())
            table = []
            for i in range(len(dictionary['tipo_proceso_tb'])):
                tipo = 'Lineas' if dictionary['tipo_proceso_tb'][i] == 'LN' else 'Estaciones de Trabajo'
                estado = 'Activo' if dictionary['estado_proceso_tb'][i] == '1' else 'Inactivo'
                my_list = [tipo+'<input type="text" id="id_tipo_proceso_tb" value="'+dictionary['tipo_proceso_tb'][i]+'" name="tipo_proceso_tb" hidden="true">',
                           dictionary['nombre_proceso_tb'][i]+'<input type="text" id="id_nombre_proceso_tb" value="'+str(dictionary['nombre_proceso_tb'][i])+'" name="nombre_proceso_tb" hidden="true">',
                           dictionary['descripcion_proceso_tb'][i]+'<input type="text" id="id_descripcion_proceso_tb" value="'+dictionary['descripcion_proceso_tb'][i]+'" name="descripcion_proceso_tb" hidden="true">',
                           estado +'<input type="text" id="id_estado_proceso_tb" value="'+str(dictionary['estado_proceso_tb'][i])+'" name="estado_proceso_tb" hidden="true">',
                           buttons]
                table.append(my_list)
            kwargs['first_table'] = table
        if 'actividad_caev_tb' in self.request.POST:
            dictionary = dict(self.request.POST.lists())
            table = []
            for i in range(len(dictionary['actividad_caev_tb'])):
                my_list = [dictionary['actividad_caev_tb'][i]+'<input type="text" id="id_actividad_caev_tb" value="'+dictionary['actividad_caev_tb'][i]+'" name="actividad_caev_tb" hidden="true">',
                buttons]
                table.append(my_list)
            kwargs['second_table'] = table
        sub_object = SubUnidadEconomica.objects.filter(unidad_economica__rif=self.request.user.username)
        sub_object = sub_object.exclude(tipo_sub_unidad='Se',sede_servicio=False).first()
        kwargs['sub_object'] = sub_object
        return super(SubUnidadEconomicaCreate, self).get_context_data(**kwargs)

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
        #user = User.objects.get(self.request.user);
        unidad_economica = UnidadEconomica.objects.filter(user_id=self.request.user.id).get()

        ## Se crea y se guarda el modelo de directorio
        directorio = Directorio()
        directorio.tipo_vialidad = form.cleaned_data['tipo_vialidad']
        directorio.nombre_vialidad = form.cleaned_data['nombre_vialidad']
        directorio.tipo_edificacion = form.cleaned_data['tipo_edificacion']
        directorio.descripcion_edificacion = form.cleaned_data['descripcion_edificacion']
        directorio.tipo_subedificacion = form.cleaned_data['tipo_subedificacion']
        directorio.descripcion_subedificacion = form.cleaned_data['descripcion_subedificacion']
        directorio.tipo_zonificacion = form.cleaned_data['tipo_zonificacion']
        directorio.nombre_zona = form.cleaned_data['nombre_zona']
        directorio.parroquia = parroquia
        directorio.usuario = self.request.user
        #directorio.coordenadas = form.cleaned_data['coordenada']
        directorio.save()
        
        ## Se crea y se guarda el modelo de sub_unidad_economica
        self.object = form.save(commit=False)
        self.object.nombre_sub = form.cleaned_data['nombre_sub']
        self.object.telefono = form.cleaned_data['telefono']
        self.object.tipo_sub_unidad = form.cleaned_data['tipo_sub_unidad']
        self.object.tipo_tenencia = form.cleaned_data['tipo_tenencia']
        self.object.m2_construccion = form.cleaned_data['m2_construccion']
        self.object.m2_terreno = form.cleaned_data['m2_terreno']
        self.object.autonomia_electrica = form.cleaned_data['autonomia_electrica']
        self.object.consumo_electrico = form.cleaned_data['consumo_electrico']
        self.object.cantidad_empleados = form.cleaned_data['cantidad_empleados']
        if(form.cleaned_data['sede_servicio']=='True'):
            self.object.sede_servicio = form.cleaned_data['sede_servicio']
        self.object.unidad_economica = unidad_economica
        self.object.save()
        
        # Si el objeto creado presta servicio, se crea un proceso llamado servicio
        if(self.object.sede_servicio):
            self.crear_servicio(self.object)
        
        ## Si el tipo de sub unidad es distinto de sede
        if(form.cleaned_data['tipo_sub_unidad']!='Se'):
        
            ## Se crea y se guarda la tabla intermedio entre directorio-sub unidad
            directorio_subunidad = SubUnidadEconomicaDirectorio()
            directorio_subunidad.directorio = directorio
            directorio_subunidad.sub_unidad_economica = self.object
            directorio_subunidad.save()
            
            if(form.cleaned_data['tipo_sub_unidad']=='Pl'):
                ## Se llama a la función que creará los procesos
                self.agregar_proceso(dictionary,self.object)
            
            ## Se llama a la función que creará las actividades economicas
            if('actividad_caev_tb' in dictionary):
                self.agregar_actividad(dictionary,self.object)
            
            caev = CaevRama.objects.get(pk=form.cleaned_data['actividad_caev_primaria'])
            ## Se crea y se guarda en el modelo del capacidad de la sub-unidad
            capacidad = SubUnidadEconomicaCapacidad()
            capacidad.caev = caev
            capacidad.capacidad_instalada_texto = form.cleaned_data['capacidad_instalada_texto']
            capacidad.capacidad_instalada_medida = form.cleaned_data['capacidad_instalada_medida']
            capacidad.capacidad_utilizada = form.cleaned_data['capacidad_utilizada']
            capacidad.sub_unidad_economica = self.object
            capacidad.save()
        
        
        return super(SubUnidadEconomicaCreate, self).form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return super(SubUnidadEconomicaCreate, self).form_invalid(form)
    
    
    def agregar_proceso(self, dictionary, model):
        """!
        Metodo que extrae los datos de la tabla de procesos en un diccionario y las guarda en el modelo respectivo
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 09-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param dictionary <b>{object}</b> Objeto que contiene el diccionario a procesar
        @param model <b>{object}</b> Objeto que contiene el modelo al que se hace la referencia
        """
        for i in range(0,len(dictionary['nombre_proceso_tb'])):
            ## Se crea y se guarda en el modelo del proceso de la sub-unidad
            proceso = SubUnidadEconomicaProceso()
            proceso.tipo_proceso = dictionary['tipo_proceso_tb'][i]
            proceso.nombre_proceso = dictionary['nombre_proceso_tb'][i]
            proceso.descripcion_proceso = dictionary['descripcion_proceso_tb'][i]
            proceso.estado_proceso = int(dictionary['estado_proceso_tb'][i])
            proceso.sub_unidad_economica = model
            proceso.save()
            
    def crear_servicio(self, model):
        """!
        Metodo que crea como servicio un proceso
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 30-11-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param model <b>{object}</b> Objeto que contiene el modelo al que se hace la referencia
        @return Retorna el formulario validado
        """
        
        ## Se crea y se guarda en el modelo del proceso de la sub-unidad
        proceso = SubUnidadEconomicaProceso()
        proceso.tipo_proceso = "OT"
        proceso.nombre_proceso = "Servicio"
        proceso.descripcion_proceso = "Prestación de un servicio"
        proceso.estado_proceso = 1
        proceso.sub_unidad_economica = model
        proceso.save()
            
    def agregar_actividad(self, dictionary, model):
        """!
        Metodo que extrae los datos de la tabla de actividades economicas en un diccionario y las guarda en el modelo respectivo
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 09-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param dictionary <b>{object}</b> Objeto que contiene el diccionario a procesar
        @param model <b>{object}</b> Objeto que contiene el modelo al que se hace la referencia
        """
        for i in range(0,len(dictionary['actividad_caev_tb'])):
            ## Se crea y se guarda en el modelo del proceso de la sub-unidad
            actividad_economica = SubUnidadEconomicaActividad()
            actividad_economica.sub_unidad_economica = model
            caev = CaevRama.objects.get(pk=dictionary['actividad_caev_tb'][i])
            actividad_economica.caev = caev
            actividad_economica.save()
            
            
def subunidad_get_data(request):
    """!
    Metodo que extrae los datos de la subunidad relacionada con el usuario y la muestra en una url ajax como json

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 04-10-2016
    @param request <b>{object}</b> Recibe la peticion
    @return Retorna el json con las subunidades que consiguió
    """
    datos = {'data':[]}
    dic_ten = dict(TIPO_TENENCIA)
    dic_sub = dict(TIPO_SUB_UNIDAD)
    for subunidad in SubUnidadEconomica.objects.filter(unidad_economica_id__user_id=request.user.id).all():
        lista = []
        lista.append(subunidad.nombre_sub)
        lista.append(subunidad.telefono)
        lista.append(str(dic_ten.get(subunidad.tipo_tenencia)))
        lista.append(str(dic_sub.get(subunidad.tipo_sub_unidad)))
        lista.append(subunidad.cantidad_empleados)
        lista.append("Si" if subunidad.sede_servicio else "No")
        datos['data'].append(lista)
    
    return JsonResponse(datos,safe=False)
            