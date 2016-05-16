from django.views.generic import CreateView
from unidad_economica.informacion_mercantil.forms import CapitalAccionistaForms
from unidad_economica.informacion_mercantil.models import CapitalAccionista

class MercantilCreate(CreateView):
    model = CapitalAccionista
    form_class = CapitalAccionistaForms
    template_name = 'informacion.mercantil.registro.html'
