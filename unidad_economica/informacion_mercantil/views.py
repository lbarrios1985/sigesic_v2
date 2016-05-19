from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import CreateView
from unidad_economica.informacion_mercantil.forms import CapitalAccionistaForms
from unidad_economica.informacion_mercantil.models import CapitalAccionista

class MercantilCreate(CreateView):

    model = CapitalAccionista
    form_class = CapitalAccionistaForms
    template_name = 'informacion.mercantil.registro.html'

    def get(self,request):
        form = CapitalAccionistaForms()
        return render_to_response('informacion.mercantil.registro.html', {'form': form}, context_instance=RequestContext(request))
    def post(self,request):

        form = CapitalAccionistaForms(request.POST)


        if(form.is_valid()):

            self.model_naturaleza_juridica = form.request.POST['naturaleza_juridica']
            self.model_naturaleza_juridica_otros = form. request.POST['naturaleza_juridica_otros']
            self.model_capital_suscrito = form. request.POST['capital_suscrito']
            self.model_capital_pagado = form. request.POST['capital_pagado']
            self.model_publico_nacional = form. request.POST['publico_nacional']
            self.model_publico_extranjero = form. request.POST['publico_extranjero']
            self.model_privado_nacional = form. request.POST['privado_nacional']
            self.model_privado_extranjero = form. request.POST['privado_extranjero']
            self.model_nombre_accionista = form. request.POST['nombre_accionista']
            self.model_save()
            return render_to_response('informacion.mercantil.registro.html', context_instance=RequestContext(request))