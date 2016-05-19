"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace sedes_admin.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo sedes_admin
# @author Hugo Ramirez (hramirez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
from django.views.generic import CreateView
from .forms import RegistroSedesForm
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica,SubUnidadEconomicaDirectorio
from unidad_economica.directorio.models import Directorio



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
    model = SubUnidadEconomica
    form_class = RegistroSedesForm
    template_name = 'sedes-admin.registrar.html'

    def form_valid(self, form):
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
        ## Se crea y se guarda el modelo de directorio
        directorio = Directorio()
        directorio.prefijo_uno=form.cleaned_data['prefijo_uno'],
        directorio.direccion_uno=form.cleaned_data['direccion_uno'],
        directorio.prefijo_dos=form.cleaned_data['prefijo_dos'],
        directorio.direccion_dos=form.cleaned_data['direccion_dos'],
        directorio.prefijo_tres=form.cleaned_data['prefijo_tres'],
        directorio.direccion_tres=form.cleaned_data['direccion_tres'],
        directorio.prefijo_cuatro=form.cleaned_data['prefijo_cuatro'],
        directorio.direccion_cuatro=form.cleaned_data['direccion_cuatro'],
        directorio.parroquia = form.cleaned_data['parroquia']
        directorio.activo=True
        directorio.save()

        ## Se crea y se guarda el modelo de sub_unidad_economica
        self.object = form.save(commit=False)
        self.object.nombre_sub = form.cleaned_data['nombre_sub']
        #self.object.tipo_coordenada = form.cleaned_data['tipo_coordenada']
        self.object.coordenada_geografica = form.cleaned_data['coordenada_geografica']
        self.object.telefono = form.cleaned_data['telefono']
        #modelSubUnidad.tipo_tenencia_id = form.cleaned_data['tipo_tenencia']
        self.object.m2_contruccion = form.cleaned_data['m2_contruccion']
        self.object.m2_terreno = form.cleaned_data['m2_terreno']
        self.object.autonomia_electrica = form.cleaned_data['autonomia_electrica']
        self.object.consumo_electrico = form.cleaned_data['consumo_electrico']
        self.object.cantidad_empleados = form.cleaned_data['cantidad_empleados']
        self.object.sede_servicio = form.cleaned_data['sede_servicio']
        self.object.directorio = directorio
        self.object.save()

        ## Se crea y se guarda la tabla intermedio entre directorio-sub unidad
        directorio_subunidad = SubUnidadEconomicaDirectorio()
        directorio_subunidad.directorio = directorio
        directorio_subunidad.sub_unidad_economica = self.object
        directorio_subunidad.save()

        return super(SedesCreate, self).form_valid(form)