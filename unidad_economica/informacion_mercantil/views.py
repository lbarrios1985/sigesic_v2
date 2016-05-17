from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import CreateView
from unidad_economica.informacion_mercantil.forms import CapitalAccionistaForms
from unidad_economica.informacion_mercantil.models import CapitalAccionista






class MercantilCreate(CreateView):
    """!
    Clase que registra usuarios en el sistema

    @author Ing. Lully Troconis (ltroconis at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 25-04-2016
    @version 2.0.0
    """
    model = CapitalAccionista
    form_class = CapitalAccionistaForms
    template_name = 'informacion.mercantil.registro.html'

    def get(self,request):
        form_name = CapitalAccionistaForms()
        return render_to_response('informacion.mercantil.registro.html', {'form':form_name}, context_instance=RequestContext(request))

    def post(self,request):
        form = CapitalAccionistaForms(request.POST)

        if(form.is_valid()):
            self.object = form.save(commit=False)
            self.object.naturaleza_juridica = form.cleaned_data['naturaleza_juridica']
            self.object.save()

            return render_to_response('informacion.mercantil.registro.html', {'form':form}, context_instance=RequestContext(request))