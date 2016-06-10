from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from base.constant import CREATE_MESSAGE
from .forms import maquinaria
from .models import mimodelo
from .forms import maquinaria
# Create your views here.
class vista(CreateView):

    model = mimodelo
    form_class = maquinaria
    template_name = 'maquinaria.equipo.base.html'
    success_url = reverse_lazy('equipos')
    success_message = CREATE_MESSAGE

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.nombre_maquinaria = form.cleaned_data['nombre_maquinaria']
        self.object.pais_origen = form.cleaned_data['pais_origen']
        self.object.descripcion_maquinaria = form.cleaned_data['descripcion_maquinaria']
        self.object.año_fabricacion = form.cleaned_data['año_fabricacion ']
        self.object.save()

        return super(vista, self).form_valid(form)