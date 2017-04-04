"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidadeconomica.views
#
# Clases, atributos, métodos y/o funciones a implementar para las vistas del módulo unidadeconomica
# @author Eveli Ramírez (eramirez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 04-05-2016
# @version 2.0
from __future__ import unicode_literals
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.forms import inlineformset_factory
from django.views.generic import CreateView, TemplateView
from django.shortcuts import render

from base.constant import CREATE_MESSAGE, UPDATE_MESSAGE
from base.classes import Seniat
from base.models import (
    CaevClase, Estado, Municipio, Parroquia, TipoComunal, Pais
    )

from unidad_economica.directorio.models import Directorio

from .forms import UnidadEconomicaForm
from .models import (
    ActividadCaev, Franquicia, UnidadEconomica, UnidadEconomicaDirectorio
    )

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


class UnidadEconomicaCreate(SuccessMessageMixin, CreateView):
    """!
    Clase que registra los datos de la unidad económica

    @author Eveli Ramírez (eramirez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 04-05-2016
    @version 2.0
    """
    model = UnidadEconomica
    form_class = UnidadEconomicaForm
    template_name = "unidad.economica.registro.html"
    success_url = reverse_lazy('informacion_mercantil')
    success_message = CREATE_MESSAGE

    def get_form_kwargs(self):
        """!
        Metodo que permite guardar el username en los kwargs
    
        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 06-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el kwargs con el username
        """
        kwargs = super(UnidadEconomicaCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        """!
        Método usado para extraer los datos del usuario logeado en el sistema
    
        @author Eveli Ramírez (eramirez at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 09-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna los datos del rif
        """
        rif = self.request.user
        datos_iniciales = super(UnidadEconomicaCreate, self).get_initial()
        datos_iniciales['rif'] = self.request.user.username

        datos_rif = Seniat()
        seniat = datos_rif.buscar_rif(rif)
        datos_iniciales['nombre_ue'] = datos_rif.nombre
        datos_iniciales['razon_social'] = datos_rif.nombre

        #carga la direccion fiscal de la unidad_economica
        if UnidadEconomicaDirectorio.objects.filter(unidad_economica__rif=rif):
            value = UnidadEconomicaDirectorio.objects.filter(unidad_economica__rif=rif).get()
            datos_iniciales['tipo_vialidad'] = value.directorio.tipo_vialidad
            datos_iniciales['nombre_vialidad'] = value.directorio.nombre_vialidad
            datos_iniciales['tipo_edificacion'] = value.directorio.tipo_edificacion
            datos_iniciales['descripcion_edificacion'] = value.directorio.descripcion_edificacion
            datos_iniciales['tipo_subedificacion'] = value.directorio.tipo_subedificacion
            datos_iniciales['descripcion_subedificacion'] = value.directorio.descripcion_subedificacion
            datos_iniciales['tipo_zonificacion'] = value.directorio.tipo_zonificacion
            datos_iniciales['nombre_zona'] = value.directorio.nombre_zona
            datos_iniciales['parroquia'] = value.directorio.parroquia
            datos_iniciales['municipio'] = value.directorio.parroquia.municipio
            datos_iniciales['estado'] = value.directorio.parroquia.municipio.estado
            if value.directorio.coordenadas != None:
                datos_iniciales['coordenada'] = value.directorio.coordenadas.split(",")

        #carga la actividad economica principal
        if ActividadCaev.objects.filter(unidad_economica_rif__rif=rif, principal=True):
            value = ActividadCaev.objects.filter(unidad_economica_rif__rif=rif, principal=True).get()
            datos_iniciales['actividad'] = value.caev.clase

        #carga los datos correspondientes a la unidad_economica
        if UnidadEconomica.objects.filter(rif=rif):
            value = UnidadEconomica.objects.filter(rif=rif).get()
            datos_iniciales['pagina_web'] = value.pagina_web
            datos_iniciales['telefono'] = value.telefono
            datos_iniciales['correo'] = value.correo
            datos_iniciales['exportador'] = value.exportador
            datos_iniciales['orga_comunal'] = value.orga_comunal
            datos_iniciales['tipo_comunal'] = value.tipo_comunal
            datos_iniciales['situr'] = value.situr
            datos_iniciales['casa_matriz_franquicia'] = value.casa_matriz_franquicia
            datos_iniciales['nro_franquicia'] = value.nro_franquicia
            datos_iniciales['franquiciado'] = value.franquiciado

        #cargar los campos del modelo franquicia en el formulario unidad_economica
        if Franquicia.objects.filter(unidad_economica_rif__rif=rif):
            value = Franquicia.objects.filter(unidad_economica_rif__rif=rif).get()
            datos_iniciales['pais_franquicia'] = value.pais_franquicia.id
            datos_iniciales['rif_casa_matriz'] = value.rif_casa_matriz
            datos_iniciales['nombre_franquicia'] = value.nombre_franquicia

        #print(datos_iniciales)

        return datos_iniciales

    def get_context_data(self, **kwargs):
        if 'actividad2_tb' in self.request.POST:
            buttons = '<a class="update_item" style="cursor: pointer"><i class="glyphicon glyphicon-pencil"></i></a>'
            buttons += '<a class="remove_item" style="cursor: pointer"><i class="glyphicon glyphicon-remove"></i></a>'
            dictionary = dict(self.request.POST.lists())
            table = []
            for i in range(len(dictionary['actividad2_tb'])):
                my_list = [
                    dictionary['actividad2_tb'][i]+'<input type="text" id="id_actividad2_tb" value="'+
                    dictionary['actividad2_tb'][i]+'" name="actividad2_tb" hidden="true">',
                    buttons
                ]
                table.append(my_list)
            kwargs['first_table'] = table
        kwargs['object_list'] = ActividadCaev.objects.all()

        #rutina para poder cargar las actividades que ya tiene la unidad_economica registradas
        if ActividadCaev.objects.filter(unidad_economica_rif__rif=self.request.user.username, principal=False):
            buttons = '<a class="update_item" style="cursor: pointer"><i class="glyphicon glyphicon-pencil"></i></a>'
            buttons += '<a class="remove_item" style="cursor: pointer"><i class="glyphicon glyphicon-remove"></i></a>'
            table = []
            for value in ActividadCaev.objects.filter(unidad_economica_rif__rif=self.request.user.username, principal=False).all():
                my_list = [
                    value.caev.descripcion+'<input type="text" id="id_actividad2_tb" value="'+
                    value.caev.descripcion+'" name="actividad2_tb" hidden="true">',
                    buttons
                ]
                table.append(my_list)
            kwargs['first_table'] = table
        return super(UnidadEconomicaCreate, self).get_context_data(**kwargs)

    def form_valid(self, form):
        """!
        Método que verifica si el formulario es válido, en cuyo caso procede a registrar los datos de la unidad económica
        
        @author Eveli Ramírez (eramirez at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 18-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """

        ## Obtiene los datos seleccionados en Parroquia
        parroquia = Parroquia.objects.get(pk=self.request.POST['parroquia'])

        ## Almacena en el modelo de Directorio
        directorio = Directorio()
        directorio.tipo_vialidad=form.cleaned_data['tipo_vialidad']
        directorio.nombre_vialidad=form.cleaned_data['nombre_vialidad']
        directorio.tipo_edificacion=form.cleaned_data['tipo_edificacion']
        directorio.descripcion_edificacion=form.cleaned_data['descripcion_edificacion']
        directorio.tipo_subedificacion=form.cleaned_data['tipo_subedificacion']
        directorio.descripcion_subedificacion=form.cleaned_data['descripcion_subedificacion']
        directorio.tipo_zonificacion=form.cleaned_data['tipo_zonificacion']
        directorio.nombre_zona=form.cleaned_data['nombre_zona']
        if form.cleaned_data['coordenada']:
            directorio.coordenadas = form.cleaned_data['coordenada']
        directorio.parroquia = parroquia
        directorio.activo=True
        directorio.usuario = self.request.user
        directorio.save()

        ## Almacena en el modelo de UnidadEconomica
        self.object = form.save(commit=False)
        self.object.rif = form.cleaned_data['rif']
        self.object.nombre_ue = form.cleaned_data['nombre_ue']
        self.object.razon_social = form.cleaned_data['razon_social']
        self.object.pagina_web= form.cleaned_data['pagina_web']
        self.object.telefono= form.cleaned_data['telefono']
        self.object.correo= form.cleaned_data['correo']
        if form.cleaned_data['orga_comunal'] == 'True':
            self.object.orga_comunal = form.cleaned_data['orga_comunal']
            tipo_comunal = TipoComunal.objects.get(pk=self.request.POST['tipo_comunal'])
            self.object.tipo_comunal = tipo_comunal
            self.object.situr = form.cleaned_data['situr']
        if form.cleaned_data['casa_matriz_franquicia'] == 'True':
            self.object.casa_matriz_franquicia = form.cleaned_data['casa_matriz_franquicia']
            self.object.nro_franquicia = form.cleaned_data['nro_franquicia']
        else:
            self.object.nro_franquicia = 0

        #self.object.nro_franquicia = form.cleaned_data['nro_franquicia']
        if form.cleaned_data['franquiciado'] == 'True':
            self.object.franquiciado = form.cleaned_data['franquiciado']
        self.object.user = self.request.user
        self.object.save()

        ## Almacena en el modelo de relación de dirección y unidad económica
        direccion = UnidadEconomicaDirectorio()
        direccion.unidad_economica = self.object
        direccion.directorio = directorio
        direccion.save()

        ## Almacena en el modelo Franquicia
        if form.cleaned_data['franquiciado'] == 'True':
            franquicia = Franquicia()
            if form.cleaned_data['rif_casa_matriz']:
                franquicia.rif_casa_matriz = "%s%s%s" % (
                        self.request.POST['rif_casa_matriz_0'], self.request.POST['rif_casa_matriz_1'], self.request.POST['rif_casa_matriz_2']
                    )
            pais = Pais.objects.get(pk=form.cleaned_data['pais_franquicia'])
            franquicia.nombre_franquicia = form.cleaned_data['nombre_franquicia']
            franquicia.pais_franquicia = pais
            franquicia.unidad_economica_rif = self.object
            franquicia.save()

        ## Obtiene los datos seleccionados en CAEV
        caev = CaevClase.objects.get(pk=self.request.POST['actividad'])

        ## Almacena en la tabla ActividadCaev
        actividad_caev = ActividadCaev()
        actividad_caev.caev = caev
        actividad_caev.unidad_economica_rif = self.object
        actividad_caev.save()

        dictionary = dict(self.request.POST.lists())
        
        if 'actividad2_tb' in dictionary.keys():
            for i in dictionary['actividad2_tb']:
                ## Obtiene los datos seleccionados en Caev
                caev = CaevClase.objects.get(pk=i)

                ## Almacena en la tabla ActividadCaev
                actividad_caev = ActividadCaev()
                actividad_caev.caev = caev
                actividad_caev.principal = False
                actividad_caev.unidad_economica_rif = self.object
                actividad_caev.save()

        return super(UnidadEconomicaCreate, self).form_valid(form)

    def form_invalid(self, form):
        #print(form.errors)
        return super(UnidadEconomicaCreate, self).form_invalid(form)
