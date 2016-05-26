
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
from django.views.generic import CreateView
from base.classes import Seniat
from unidad_economica.informacion_mercantil.forms import InformacionMercantilForms
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from unidad_economica.informacion_mercantil.models import Capital, Accionista, RepresentanteLegal
from base.constant import (
    CREATE_MESSAGE, CADUCIDAD_LINK_REGISTRO, REGISTRO_MESSAGE, EMAIL_SUBJECT_REGISTRO, UPDATE_MESSAGE
)


@login_required
def siguiente(request):
    return render_to_response('sedes-admin.registrar.html', {}, context_instance=RequestContext(request))


class MercantilCreate(CreateView):
    """!
    Clase que gestiona los procesos mercantiles

    @author Lully Troconis (ltroconis at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 25-04-2016
    @version 2.0.0
    """

    model = Capital
    form_class = InformacionMercantilForms
    template_name = 'informacion.mercantil.registro.html'
    success_url = reverse_lazy('sede_administrativa')
    success_message = CREATE_MESSAGE

    def get_initial(self):
        rif = self.request.user
        datos = super(MercantilCreate, self).get_initial()
        datos['rif_accionista'] = self.request.user.username

        datos_rif = Seniat()
        seniat = datos_rif.buscar_rif(rif)
        datos['nombre'] = datos_rif.nombre

        return datos

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
        print("Es válido")

        self.object = form.save(commit=False)
        #self.object.rif_ue = form.cleaned_data['rif_ue']
        self.object.naturaleza_juridica = form.cleaned_data['naturaleza_juridica']
        self.object.naturaleza_juridica_otros = form.cleaned_data['naturaleza_juridica_otros']
        self.object.capital_suscrito = form.cleaned_data['capital_suscrito']
        self.object.capital_pagado = form.cleaned_data['capital_pagado']
        self.object.publico_nacional = form.cleaned_data['publico_nacional']
        self.object.publico_extranjero = form.cleaned_data['publico_extranjero']
        self.object.privado_nacional = form.cleaned_data['privado_nacional']
        self.object.privado_extranjero = form.cleaned_data['privado_extranjero']
        self.object.save()

        Accionista.objects.create(
            #rif_ue=form.cleaned_data['rif_ue'],
            rif_accionista=form.cleaned_data['rif_accionista'],
            nombre=form.cleaned_data['nombre'],
            porcentaje=form.cleaned_data['porcentaje'],
        )

        RepresentanteLegal.objects.create(
            #rif_ue=form.cleaned_data['rif_ue'],
            cedula_representante=form.cleaned_data['cedula_representante'],
            nombre_representante=form.cleaned_data['nombre_representante'],
            apellido_representante=form.cleaned_data['apellido_representante'],
            correo_electronico=form.cleaned_data['correo_electronico'],
            telefono=form.cleaned_data['telefono'],
            cargo=form.cleaned_data['cargo'],

        )

        return super(MercantilCreate, self).form_valid(form)

    def form_invalid(self, form):
        print("Es inválido")
        print(form)
        return super(MercantilCreate, self).form_invalid(form)