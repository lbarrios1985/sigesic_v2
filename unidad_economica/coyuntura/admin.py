"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package unidad_economica.coyuntura.admin
#
# Clases, atributos y métodos del módulo coyuntura a implementar en el panel administrativo 
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 22-09-2016
# @version 2.0

from __future__ import unicode_literals
from django.contrib import admin
from .forms import PeriodicidadAdminForm, MesAdminForm, TrimestreAdminForm
from .models import PeriodicidadAdmin, MesAdmin, TrimestreAdmin, AnhoAdmin
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomicaActividad, SubUnidadEconomicaDirectorio
import logging
logger = logging.getLogger("coyuntura")

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

class MesAdministrador(admin.ModelAdmin):
    form= MesAdminForm
    list_display = ('enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre')

class TrimestreAdministrador(admin.ModelAdmin):
    form= TrimestreAdminForm
    list_display = ('trimestre_1','trimestre_2','trimestre_3','trimestre_4')

class AnhoAdministrador(admin.ModelAdmin):
    list_display = ('anho',)

class PeriodicidadAdministrador(admin.ModelAdmin):
    """!
    Clase que gestiona la Periodicidad del módulo de coyuntura en el panel administrativo

    @author Ing. William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 18-01-2017
    @version 2.0.0
    """

    def save_model(self, request, obj, form, change):
        """!
        Método para guardar de forma personalizada en el modelo
    
        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 18-01-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto con los datos
        @param obj <b>{object}</b> Objeto donde se guardan los datos
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @param change <b>{object}</b>
        @return No retorna nada
        """

        # custom stuff here
        obj = form.save(commit=False)
        obj.periodo= form.cleaned_data['periodo']

        if form.cleaned_data['periodo'] == 'M':
            obj.mes= MesAdmin.objects.get(pk=form.cleaned_data['mes'])
            obj.trimestre= None
        elif form.cleaned_data['periodo'] == 'T':
            obj.mes= None
            obj.trimestre= TrimestreAdmin.objects.get(pk=form.cleaned_data['trimestre'])

        obj.anho= AnhoAdmin.objects.get(pk=form.cleaned_data['anho'])

        ## esta condicion agrega periodicidad a todas las sub_unidad_economica que hacen la actividad caev dada
        if form.cleaned_data['tipo_consulta'] == 'caev':
            for sue in SubUnidadEconomicaActividad.objects.filter(caev_id=form.cleaned_data['caev']).all():
                periodicidad_admin = PeriodicidadAdmin()
                periodicidad_admin.periodo = obj.periodo
                periodicidad_admin.mes = obj.mes
                periodicidad_admin.trimestre = obj.trimestre
                periodicidad_admin.anho = obj.anho
                sue = SubUnidadEconomica.objects.get(pk=sue.sub_unidad_economica_id)
                obj.sub_unidad_economica= sue
                periodicidad_admin.sub_unidad_economica = obj.sub_unidad_economica
                periodicidad_admin.save()

        ## esta condicion agrega periodicidad a todas las sub_unidad_economica que pertenecen a una unidad_economica dada
        elif form.cleaned_data['tipo_consulta'] == 'ue':
            for sue in SubUnidadEconomica.objects.filter(unidad_economica_id=form.cleaned_data['ue']).all():
                periodicidad_admin = PeriodicidadAdmin()
                periodicidad_admin.periodo = obj.periodo
                periodicidad_admin.mes = obj.mes
                periodicidad_admin.trimestre = obj.trimestre
                periodicidad_admin.anho = obj.anho
                obj.sub_unidad_economica = sue
                periodicidad_admin.sub_unidad_economica = obj.sub_unidad_economica
                periodicidad_admin.save()

        ## esta condicion agrega periodicidad a todas las sub_unidad_economica que pertenecen a un estado dado
        elif form.cleaned_data['tipo_consulta'] == 'e':
            for sue in SubUnidadEconomicaDirectorio.objects.filter(directorio__parroquia__municipio__estado_id=form.cleaned_data['estado']).all():
                print(sue.sub_unidad_economica)
                periodicidad_admin = PeriodicidadAdmin()
                periodicidad_admin.periodo = obj.periodo
                periodicidad_admin.mes = obj.mes
                periodicidad_admin.trimestre = obj.trimestre
                periodicidad_admin.anho = obj.anho
                obj.sub_unidad_economica = sue.sub_unidad_economica
                periodicidad_admin.sub_unidad_economica = obj.sub_unidad_economica
                periodicidad_admin.save()

    form= PeriodicidadAdminForm
    list_display = ('periodo', 'mes', 'trimestre', 'anho', 'sub_unidad_economica')
    #list_filter = ('descripcion', 'mes', 'trimestre', 'anho', 'sub_unidad_economica')
    #ordering = ('descripcion', 'mes', 'trimestre', 'anho', 'sub_unidad_economica')
    #search_fields = ('descripcion', 'mes', 'trimestre')

admin.site.register(PeriodicidadAdmin, PeriodicidadAdministrador)
admin.site.register(MesAdmin, MesAdministrador)
admin.site.register(TrimestreAdmin, TrimestreAdministrador)
admin.site.register(AnhoAdmin, AnhoAdministrador)
