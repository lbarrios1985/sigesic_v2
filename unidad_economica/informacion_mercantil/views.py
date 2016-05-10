from django.views.generic import CreateView
from unidad_economica.informacion_mercantil.forms import CapitalAccionistaForms
from unidad_economica.informacion_mercantil.models import CapitalAccionista

class mercantil (CreateView):
    model = CapitalAccionista
    form_class = CapitalAccionistaForms
    template_name = 'mercantil.html'