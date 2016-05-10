from django.views.generic import CreateView
from informacion_mercantil.forms import CapitalAccionistaForms
from informacion_mercantil.models import CapitalAccionista

class mercantil (CreateView):
    model = CapitalAccionista
    form_class = CapitalAccionistaForms
    template_name = 'mercantil.html'