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
from django.http import JsonResponse
from django.apps import apps
from django import forms
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from .models import Servicio, ServicioCliente
from .forms import ServiciosGeneralForm, ServiciosClienteForm
from base.constant import CREATE_MESSAGE, TIPO_SERVICIO
from base.models import CaevClase, Pais, Cliente, AnhoRegistro
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
    
    def form_valid(self,form):
        """!
        Metodo que valida si el formulario es valido, en cuyo caso se procede a registrar los datos del servicio
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 24-10-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        ## Se crea la instancia de caev
        caev = CaevClase.objects.get(pk=form.cleaned_data['caev'])
        ## Se crea la instancia de sub_unidad
        subunidad = SubUnidadEconomica.objects.get(pk=form.cleaned_data['subunidad'])
        
        ## Se crea y se guarda el modelo de facturacion del cliente
        self.object = form.save(commit=False)
        self.object.nombre_servicio = form.cleaned_data['nombre_servicio']
        self.object.tipo_servicio = form.cleaned_data['tipo_servicio']
        self.object.caev = caev
        self.object.cantidad_clientes = form.cleaned_data['cantidad_clientes']
        self.object.subunidad = subunidad
        self.object.save()
        
        return super(ServiciosGeneralesCreate, self).form_valid(form)
    
    def form_invalid(self,form):
        return super(ServiciosGeneralesCreate, self).form_invalid(form)
    
    
def servicios_get_data(request):
    """!
    Metodo que extrae los datos de los servicios relacionados con la subunidad y la muestra en una url ajax como json

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 20-10-2016
    @param request <b>{object}</b> Recibe la peticion
    @return Retorna el json con las subunidades que consiguió
    """
    datos = {'data':[]}
    # Recibe por get el id del producto
    subid = request.GET.get('subunidad_id', None)
    dic_ts = dict(TIPO_SERVICIO)
    if(subid):
        for serv in Servicio.objects.filter(subunidad_id=subid).all():
            lista = []
            lista.append(serv.nombre_servicio)
            lista.append(str(dic_ts.get(serv.tipo_servicio)))
            lista.append(serv.caev.pk)
            lista.append(serv.cantidad_clientes)
            lista.append(serv.subunidad.nombre_sub)
            datos['data'].append(lista)
        
        return JsonResponse(datos,safe=False)
    return JsonResponse("No se envío el id de la subunidad",safe=False)

class ServiciosClientesCreate(SuccessMessageMixin,CreateView):
    """!
    Clase que registra los servicios

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-05-2016
    @version 2.0.0
    """
    model = ServicioCliente
    form_class = ServiciosClienteForm
    template_name = "servicios.template.html"
    success_url = reverse_lazy('servicio_cliente_create')
    success_message = CREATE_MESSAGE
    
    def get_form_kwargs(self):
        """!
        Metodo que permite guardar el username en los kwargs
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 14-07-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el kwargs con el username
        """
        kwargs = super(ServiciosClientesCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def form_valid(self,form):
        """!
        Metodo que valida si el formulario es valido, en cuyo caso se procede a registrar los datos del cliente
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 25-10-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        ## Se crea la instancia del año
        anho = AnhoRegistro.objects.get(pk=form.cleaned_data['anho'])

        pais = Pais.objects.get(pk=form.cleaned_data['ubicacion_cliente'])
        servicio = Servicio.objects.get(pk=form.cleaned_data['cliente_servicio'])
        
        if(form.cleaned_data['rif']):
            ## Se busca el cliente si ya existe
            cliente = Cliente.objects.filter(rif=form.cleaned_data['rif'])
            if cliente:
                cliente = cliente.get()  
            else:
                ## Se crea y se guarda el modelo de cliente
                cliente = Cliente()
                cliente.nombre = form.cleaned_data['nombre_cliente']
                #Si es venezuela se toma en cuenta el rif
                if(pais.pk==1):
                    cliente.rif = form.cleaned_data['rif']
                cliente.pais = pais
                cliente.save()
        else:
            cliente = Cliente()
            cliente.nombre = form.cleaned_data['nombre_cliente']
            cliente.pais = pais
            cliente.save()
        
        ## Se crea y se guarda el modelo de facturacion del cliente
        self.object = form.save(commit=False)
        self.object.servicio_prestado = form.cleaned_data['servicio_prestado']
        self.object.precio = form.cleaned_data['precio']
        self.object.tipo_moneda = form.cleaned_data['tipo_moneda']
        self.object.monto_facturado = form.cleaned_data['monto_facturado']
        self.object.anho_registro = anho
        self.object.cliente = cliente
        self.object.servicio = servicio
        self.object.save()
        
        return super(ServiciosClientesCreate, self).form_valid(form)
    
    def form_invalid(self,form):
        print(form.errors)
        return super(ServiciosClientesCreate, self).form_invalid(form)

def servicios_cliente_get_data(request):
    """!
    Metodo que extrae los datos de los clientes relacionados con el servicio y la muestra en una url ajax como json

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 25-10-2016
    @param request <b>{object}</b> Recibe la peticion
    @return Retorna el json con las subunidades que consiguió
    """
    datos = {'data':[]}
    # Recibe por get el id del producto
    servid = request.GET.get('servicio_id', None)
    if(servid):
        for serv in ServicioCliente.objects.filter(servicio_id=servid).all():
            lista = []
            lista.append(serv.servicio.nombre_servicio)
            lista.append(serv.cliente.nombre)
            lista.append(serv.cliente.pais.nombre)
            lista.append(serv.cliente.rif)
            lista.append(serv.precio)
            lista.append(serv.tipo_moneda)
            lista.append(serv.monto_facturado)
            lista.append(serv.servicio_prestado)
            datos['data'].append(lista)
        
        return JsonResponse(datos,safe=False)
    return JsonResponse("No se envío el id del servicio",safe=False)
