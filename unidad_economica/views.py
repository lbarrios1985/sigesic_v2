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
    CaevClase, Estado, Municipio, Parroquia, TipoComunal
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

        return datos_iniciales

    def get_context_data(self, **kwargs):
        buttons = '<a class="update_item" style="cursor: pointer"><i class="glyphicon glyphicon-pencil"</i></a>'
        buttons += '<a class="remove_item" style="cursor: pointer"><i class="glyphicon glyphicon-remove"</i></a>'
        if 'actvidad2_tb' in self.request.POST:
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
        if form.cleaned_data['tipo_coordenada'] and form.cleaned_data['coordenada']:
            directorio.tipo_coordenada = form.cleaned_data['tipo_coordenada']
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
        self.object.orga_comunal = form.cleaned_data['orga_comunal']
        if form.cleaned_data['orga_comunal'] == 'S':
            tipo_comunal = TipoComunal.objects.get(pk=self.request.POST['tipo_comunal'])
            self.object.tipo_comunal = tipo_comunal
        self.object.situr = form.cleaned_data['situr']
        self.object.casa_matriz_franquicia = form.cleaned_data['casa_matriz_franquicia']
        self.object.nro_franquicia = form.cleaned_data['nro_franquicia']
        self.object.franquiciado = form.cleaned_data['franquiciado']
        self.object.user = self.request.user
        self.object.save()

        ## Almacena en el modelo de relación de dirección y unidad económica
        direccion = UnidadEconomicaDirectorio()
        direccion.unidad_economica = self.object
        direccion.directorio = directorio
        direccion.save()

        ## Almacena en el modelo Franquicia
        if form.cleaned_data['rif_casa_matriz']:
            franquicia = Franquicia()
            franquicia.rif_casa_matriz = "%s%s%s" % (
                    self.request.POST['rif_casa_matriz_0'], self.request.POST['rif_casa_matriz_1'], self.request.POST['rif_casa_matriz_2']
                )
            franquicia.nombre_franquicia = form.cleaned_data['nombre_franquicia']
            franquicia.pais_franquicia = form.cleaned_data['pais_franquicia']
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

        return super(UnidadEconomicaCreate, self).form_invalid(form)
