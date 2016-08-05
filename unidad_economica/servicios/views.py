"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.bienes_prod_comer.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo de servicios
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.apps import apps
from django import forms
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from .models import Servicio, TipoServicio, ServicioCliente
from .forms import ServiciosGeneralForm
from base.constant import CREATE_MESSAGE
from base.models import CaevClase, Pais
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica

class ServiciosGeneralesCreate(SuccessMessageMixin,CreateView):
    """!
    Clase que registra los servicios

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-05-2016
    @version 2.0.0
    """
    model = Servicio
    form_class = ServiciosGeneralForm
    template_name = "servicios.template.html"
    success_url = reverse_lazy('servicio_general_create')
    success_message = CREATE_MESSAGE
    
    """def get_context_data(self, **kwargs):
        data = {}
        for item in Produccion.objects.all():
            data[item.id] = {}
            data[item.id]["nombre_producto"] = item.producto.nombre_producto
            data[item.id]["especificacion_tecnica"] = item.producto.especificacion_tecnica
            data[item.id]["marca"] = item.producto.marca
            data[item.id]["caev"] = item.producto.caev.descripcion
            data[item.id]["clientes"] = item.cantidad_clientes
            data[item.id]["insumos"] = item.cantidad_insumos
            data[item.id]["cantidad"] = item.cantidad_produccion
            data[item.id]["unidad_medida"] = item.unidad_de_medida
        kwargs['producto_list'] = data
        return super(BienesGeneralesCreate, self).get_context_data(**kwargs)"""
    
    def get_form_kwargs(self):
        """!
        Metodo que permite guardar el username en los kwargs
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 14-07-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el kwargs con el username
        """
        kwargs = super(ServiciosGeneralesCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs