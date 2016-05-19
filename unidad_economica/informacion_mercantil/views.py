from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import CreateView
from base.classes import Seniat
from unidad_economica.informacion_mercantil.forms import InformacionMercantilForms
from unidad_economica.models import UnidadEconomica


class MercantilCreate(CreateView):

    model = UnidadEconomica
    form_class = InformacionMercantilForms
    template_name = 'informacion.mercantil.registro.html'

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['rif_accionista']
        #rif = self.object.username
        datos_iniciales = super(MercantilCreate, self).get_initial()
        datos_iniciales['rif_accionista'] = self.request.user.username

        datos_rif = Seniat()
        seniat = datos_rif.buscar_rif(rif)
        datos_iniciales['nombre'] = datos_rif.nombre

        return datos_iniciales