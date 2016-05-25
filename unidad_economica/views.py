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
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView

from base.constant import CREATE_MESSAGE, REGISTRO_MESSAGE, UPDATE_MESSAGE
from base.classes import Seniat
from base.models import Parroquia

from .forms import UnidadEconomicaForm
from .models import UnidadEconomica

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
    success_message = REGISTRO_MESSAGE

    def get_initial(self):
        rif = self.request.user
        datos_iniciales = super(UnidadEconomicaCreate, self).get_initial()
        datos_iniciales['rif'] = self.request.user.username

        datos_rif = Seniat()
        seniat = datos_rif.buscar_rif(rif)
        datos_iniciales['nombre_ue'] = datos_rif.nombre
        datos_iniciales['razon_social'] = datos_rif.nombre

        return datos_iniciales

    def form_valid(self, form):
        """!
        Método que valida si el formulario es valido, en cuyo caso se procede a registrar los datos de la unidad económica
        
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
        directorio.prefijo_uno=form.cleaned_data['prefijo_uno']
        directorio.direccion_uno=form.cleaned_data['direccion_uno']
        directorio.prefijo_dos=form.cleaned_data['prefijo_dos']
        directorio.direccion_dos=form.cleaned_data['direccion_dos']
        directorio.prefijo_tres=form.cleaned_data['prefijo_tres']
        directorio.direccion_tres=form.cleaned_data['direccion_tres']
        directorio.prefijo_cuatro=form.cleaned_data['prefijo_cuatro']
        directorio.direccion_cuatro=form.cleaned_data['direccion_cuatro']
        directorio.coordenadas = form.cleaned_data['coordenada']
        directorio.parroquia = parroquia
        directorio.activo=True
        directorio.save()

        ## Almacena en el modelo de UnidadEconomica
        self.object = form.save(commit=False)
        self.object.rif = form.cleaned_data['rif']
        self.object.nombre_ue = form.cleaned_data['nombre_ue']
        self.object.razon_social = form.cleaned_data['razon_social']
        self.object.directorio = directorio
        self.object.actividad = form.cleaned_data['actividad']
        self.object.nro_planta = form.cleaned_data['nro_planta']
        self.object.nro_unid_comercializadora = form.cleaned_data['nro_unid_comercializadora']
        self.object.servicio = form.cleaned_data['servicio']
        self.object.orga_comunal = form.cleaned_data['orga_comunal']
        self.object.tipo_comunal = form.cleaned_data['tipo_comunal']
        self.object.situr = form.cleaned_data['situr']
        self.object.casa_matriz_franquicia = form.cleaned_data['casa_matriz_franquicia']
        self.object.nro_franquicia = form.cleaned_data['nro_franquicia']
        self.object.franquiciado = form.cleaned_data['franquiciado']
        self.object.save()

        ## Almacena en el modelo Franquicia
        franquicia = Franquicia()
        franquicia.pais_franquicia = form.cleaned_data['pais_franquicia']
        franquicia.nombre_franquicia = form.cleaned_data['nombre_franquicia']
        franquicia.rif_franquicia = form.cleaned_data['rif_franquicia']
        franquicia.unidad_economica_rif = self.object
        franquicia.save()

        return super(UnidadEconomicaCreate, self).form_valid(form)

