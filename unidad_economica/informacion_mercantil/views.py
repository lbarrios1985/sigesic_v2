
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
from unidad_economica.models import UnidadEconomica


class MercantilCreate(CreateView):
    """!
    Clase que gestiona los procesos mercantiles

    @author Lully Troconos (ltroconis at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 25-04-2016
    @version 2.0.0
    """

    model = UnidadEconomica
    form_class = InformacionMercantilForms
    template_name = 'informacion.mercantil.registro.html'

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['rif_accionista']
        #rif = self.object.username
        datos = super(MercantilCreate, self).get_initial()
        datos['rif_accionista'] = self.request.user.username

        datos_rif = Seniat()
        seniat = datos_rif.buscar_rif(rif)
        datos['nombre'] = datos_rif.nombre

        return datos
"""
    def form_valid(self, form):

        Método que valida si el formulario es válido

        @author Lully Troconis (ltroconis at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 18-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado

        self.object = form.save(commit=False)
        self.object.rif = form.cleaned_data['rif']
        self.object.naturaleza_juridica = form.cleaned_data['naturaleza_juridica']
        self.object.naturaleza_juridica_otros = form.cleaned_data['naturaleza_juridica_otros']
        self.object.naturaleza_juridica_otros = form.cleaned_data['capital_suscrito']
        self.object.save()


        return super(MercantilCreate, self).form_valid(form)
"""