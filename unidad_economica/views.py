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
from django.core.urlresolvers import reverse_lazy
from django.forms import inlineformset_factory
from django.views.generic import CreateView, UpdateView

from base.constant import CREATE_MESSAGE, UPDATE_MESSAGE
from base.classes import Seniat
from base.models import Ciiu, Estado, Municipio, Parroquia, TipoComunal

from unidad_economica.directorio.models import Directorio

from .forms import UnidadEconomicaForm
from .models import ActividadCiiu, Franquicia, UnidadEconomica, UnidadEconomicaDirectorio

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

    def form_valid(self, form):
        """!
        Método que verifica si el formulario es válido, en cuyo caso se procede a registrar los datos de la unidad económica
        
        @author Eveli Ramírez (eramirez at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 18-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        print("Valido..")
        print(self.request.POST)

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
        #directorio.coordenadas = form.cleaned_data['coordenada']
        directorio.parroquia = parroquia
        directorio.activo=True
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
        self.object.save()

        ## Almacena en el modelo de relación de dirección y unidad económica
        direccion = UnidadEconomicaDirectorio()
        direccion.unidad_economica = self.object
        direccion.directorio = directorio
        direccion.save()

        ## Almacena en el modelo Franquicia
        franquicia = Franquicia()
        franquicia.pais_franquicia = form.cleaned_data['pais_franquicia']
        franquicia.nombre_franquicia = form.cleaned_data['nombre_franquicia']
        franquicia.rif_casa_matriz = form.cleaned_data['rif_casa_matriz']
        franquicia.unidad_economica_rif = self.object
        franquicia.save()

        ## Obtiene los datos seleccionados en Ciiu
        ciiu = Ciiu.objects.get(pk=self.request.POST['actividad'])

        ## Almacena en la tabla ActividadCiiu
        actividad_ciiu = ActividadCiiu()
        actividad_ciiu.ciiu = ciiu
        actividad_ciiu.unidad_economica_rif = self.object
        actividad_ciiu.save()

        lista = dict(self.request.POST.lists())
        
        for i in lista['actividad2_tb']:
            ## Obtiene los datos seleccionados en Ciiu
            ciiu = Ciiu.objects.get(pk=i)

            ## Almacena en la tabla ActividadCiiu
            actividad_ciiu = ActividadCiiu()
            actividad_ciiu.ciiu = ciiu
            actividad_ciiu.unidad_economica_rif = self.object
            actividad_ciiu.save()

        return super(UnidadEconomicaCreate, self).form_valid(form)

    def form_invalid(self, form):
        print('*'*10)
        print(form)
        return super(UnidadEconomicaCreate, self).form_invalid(form)        

