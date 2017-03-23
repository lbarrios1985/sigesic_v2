
"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package informacion_mercantil.views
#
# Clases, atributos, métodos y/o funciones a implementar para las vistas del módulo unidadeconomica
# @author Lully Troconis (ltroconis at cenditel.gob.ve)
# @author <a href='​http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 04-05-2016
# @version 2.0

from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import InformacionMercantilForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import Capital, Accionista, RepresentanteLegal
from base.constant import CREATE_MESSAGE
from unidad_economica.models import UnidadEconomica
from base.classes import Seniat
from base.models import Pais

class InformacionMercantilCreate(SuccessMessageMixin, CreateView):
    """!
    Clase que gestiona los procesos mercantiles

    @author Lully Troconis (ltroconis at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 25-04-2016
    @version 2.0.0
    """

    model = Capital
    form_class = InformacionMercantilForm
    template_name = 'informacion.mercantil.registro.html'
    success_url = reverse_lazy('sub_unidad_create')
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
        kwargs = super(InformacionMercantilCreate, self).get_form_kwargs()
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
        datos_iniciales = super(InformacionMercantilCreate, self).get_initial()
        datos_iniciales['rif'] = self.request.user.username

        datos_rif = Seniat()
        seniat = datos_rif.buscar_rif(rif)

        ## carga los datos del modelo Capital
        if Capital.objects.filter(unidad_economica__rif=rif):
            value = Capital.objects.filter(unidad_economica__rif=rif).get()
            datos_iniciales['naturaleza_juridica'] = value.naturaleza_juridica
            ## convierto los float en str para reemplazar '.' por ','
            datos_iniciales['capital_suscrito'] = str(value.capital_suscrito).replace('.',',')
            datos_iniciales['capital_pagado'] = str(value.capital_pagado).replace('.',',')
            datos_iniciales['publico_nacional'] = str(value.publico_nacional).replace('.',',')
            datos_iniciales['publico_extranjero'] = str(value.publico_extranjero).replace('.',',')
            datos_iniciales['privado_nacional'] = str(value.privado_nacional).replace('.',',')
            datos_iniciales['privado_extranjero'] = str(value.privado_extranjero).replace('.',',')

        #falta cargar modelo Accionista

        ## carga los datos del modelo RepresentanteLegal
        if RepresentanteLegal.objects.filter(unidad_economica__rif=rif):
            value = RepresentanteLegal.objects.filter(unidad_economica__rif=rif).get()
            datos_iniciales['rif_representante'] = value.rif_representante
            datos_iniciales['razon_social_representante'] = value.razon_social_representante
            datos_iniciales['correo_electronico'] = value.correo_electronico
            datos_iniciales['telefono'] = value.telefono
            datos_iniciales['cargo'] = value.cargo
            datos_iniciales['cargo_otros'] = value.cargo_otros

        return datos_iniciales

    """def get_context_data(self, **kwargs):
        if Accionista.objects.filter(rif_ue__rif=self.request.user.username):
            buttons = '<a class="update_item" style="cursor: pointer"><i class="glyphicon glyphicon-pencil"></i></a>'
            buttons += '<a class="remove_item" style="cursor: pointer"><i class="glyphicon glyphicon-remove"></i></a>'
            table = []
            for value in Accionista.objects.filter(rif_ue__rif=self.request.user.username).all():
                my_list = [
                    "<td></td>",
                    "<td></td>",
                    "<td></td>",
                    "<td></td>"
                ]
                table.append(my_list)
            kwargs['first_table'] = table
        return super(InformacionMercantilCreate, self).get_context_data(**kwargs)"""

    def form_valid(self, form):

        """!
        Método que valida si el formulario es válido

        @author Lully Troconis (ltroconis at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 18-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """

        dictionary = dict(self.request.POST.lists())
        self.agregar_accionistas(dictionary,self.object)

        unidad_economica = UnidadEconomica.objects.get(rif=self.request.user)

        representante_legal= RepresentanteLegal()
        representante_legal.rif_representante= form.cleaned_data['rif_representante']
        representante_legal.razon_social_representante= form.cleaned_data['razon_social_representante']
        representante_legal.correo_electronico= form.cleaned_data['correo_electronico']
        representante_legal.telefono= form.cleaned_data['telefono']
        representante_legal.cargo= form.cleaned_data['cargo']
        representante_legal.cargo_otros= form.cleaned_data['cargo_otros']
        representante_legal.unidad_economica= unidad_economica
        representante_legal.save()

        self.object = form.save(commit=False)
        self.object.naturaleza_juridica = form.cleaned_data['naturaleza_juridica']
        self.object.capital_suscrito = form.cleaned_data['capital_suscrito']
        self.object.capital_pagado = form.cleaned_data['capital_pagado']
        self.object.publico_nacional = form.cleaned_data['publico_nacional']
        self.object.publico_extranjero= form.cleaned_data['publico_extranjero']
        self.object.privado_nacional= form.cleaned_data['privado_nacional']
        self.object.privado_extranjero= form.cleaned_data['privado_extranjero']
        self.object.unidad_economica= unidad_economica
        self.object.save()

        return super(InformacionMercantilCreate, self).form_valid(form)

    def agregar_accionistas(self, dictionary, model):
        """!
        Metodo que extrae los datos de la tabla de procesos en un diccionario y las guarda en el modelo respectivo

        @author Lully Troconis (ltroconis at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 09-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param dictionary <b>{object}</b> Objeto que contiene el diccionario a procesar
        @param model <b>{object}</b> Objeto que contiene el modelo al que se hace la referencia
        @return Retorna el formulario validado
        """

        unidad_economica = UnidadEconomica.objects.get(rif=self.request.user)

        for i in range(0,len(dictionary['razon_social_accionista_tb'])):

            ## Se crea y se guarda en el modelo del proceso de la sub-unidad
            accionista = Accionista()
            accionista.rif_accionista = dictionary['rif_accionista_tb'][i]
            accionista.nombre = dictionary['razon_social_accionista_tb'][i]

            pais= Pais.objects.get(pk=dictionary['pais_origen_tb'][i])
            accionista.pais_origen = pais

            accionista.porcentaje = int(dictionary['porcentaje_tb'][i])
            accionista.unidad_economica = unidad_economica
            accionista.save()

    def form_invalid(self, form):
        return super(InformacionMercantilCreate, self).form_invalid(form)

