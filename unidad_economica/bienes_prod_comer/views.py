"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.bienes_prod_comer.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo de bienes producidos y comercializados
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.apps import apps
from django import forms
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from .models import Producto, Produccion, Cliente, FacturacionCliente
from .forms import BienesForm, ClientesForm
from base.constant import CREATE_MESSAGE
from base.models import CaevClase, Pais
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
    
class BienesCreate(CreateView):
    """!
    Clase que registra los bienes

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 14-07-2016
    @version 2.0.0
    """
    model = Producto
    form_class = BienesForm
    template_name = "bienes.producidos.comercializados.template.html"
    success_url = reverse_lazy('bienes_generales_create')
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
        kwargs = super(BienesCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def form_valid(self,form):
        """!
        Metodo que valida si el formulario es valido, en cuyo caso se procede a registrar los datos de los bienes
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 18-07-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        subunidad = SubUnidadEconomica.objects.get(pk=form.cleaned_data['subunidad'])
        caev = CaevClase.objects.get(pk=form.cleaned_data['caev'])
        
        ## Se crea y se guarda el modelo de producto
        self.object = form.save(commit=False)
        self.object.nombre_producto = form.cleaned_data['nombre_producto']
        self.object.especificacion_tecnica = form.cleaned_data['especificacion_tecnica']
        self.object.marca = form.cleaned_data['marca']
        self.object.subunidad = subunidad
        self.object.caev = caev
        self.object.save()
        
        ## Se crea y se guarda el modelo de produccion
        produccion = Produccion()
        produccion.cantidad_produccion = form.cleaned_data['cantidad_produccion']
        produccion.unidad_de_medida = form.cleaned_data['unidad_de_medida']
        produccion.anho_registro = 2016
        produccion.cantidad_clientes = form.cleaned_data['cantidad_clientes']
        produccion.cantidad_insumos = form.cleaned_data['cantidad_insumos']
        produccion.producto = self.object
        produccion.save()
        
        return super(BienesCreate, self).form_valid(form)
    
    
def produccion_get_data(request):
    """!
    Metodo que extrae los datos de los bienes relacionados con la subunidad y la muestra en una url ajax como json

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 05-10-2016
    @param request <b>{object}</b> Recibe la peticion
    @return Retorna el json con las subunidades que consiguió
    """
    datos = {'data':[]}
    # Recibe por get el id de subunidad
    subid = request.GET.get('subunidad_id', None)
    if(subid):
        for prod in Produccion.objects.filter(producto__subunidad_id=subid,producto__subunidad__unidad_economica__user_id=request.user.id).all():
            lista = []
            lista.append(prod.producto.nombre_producto)
            lista.append(prod.producto.especificacion_tecnica)
            lista.append(prod.producto.marca)
            lista.append(prod.producto.caev.descripcion)
            lista.append(prod.cantidad_clientes)
            lista.append(prod.cantidad_insumos)
            lista.append(prod.cantidad_produccion)
            lista.append(prod.unidad_de_medida)
            datos['data'].append(lista)
        
        return JsonResponse(datos,safe=False)
    return JsonResponse("No se envío el id de la subunidad",safe=False)
 

class ClientesCreate(SuccessMessageMixin,CreateView):
    """!
    Clase que registra los bienes y clientes

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 13-07-2016
    @version 2.0.0
    """
    model = Cliente
    form_class = ClientesForm
    template_name = "bienes.producidos.comercializados.template.html"
    success_url = reverse_lazy('bienes_generales_create')
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
        kwargs = super(ClientesCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def form_valid(self,form):
        """!
        Metodo que valida si el formulario es valido, en cuyo caso se procede a registrar los datos del cliente
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 20-07-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        
        produccion = Produccion.objects.get(pk=form.cleaned_data['cliente_producto'])
        pais = Pais.objects.get(pk=form.cleaned_data['ubicacion_cliente'])
        
        ## Se crea y se guarda el modelo de cliente
        self.object = form.save(commit=False)
        self.object.nombre = form.cleaned_data['nombre_producto']
        self.object.rif = form.cleaned_data['especificacion_tecnica']
        self.object.pais = pais
        self.object.produccion = produccion
        self.object.save()
        
        ## Se crea y se guarda el modelo de facturacion del cliente
        facturacion = FacturacionCliente()
        facturacion.cantidad_produccion = form.cleaned_data['cantidad_vendida']
        facturacion.unidad_de_medida = form.cleaned_data['unidad_de_medida_cliente']
        facturacion.precio_venta_bs = form.cleaned_data['precio_venta_bs']
        facturacion.precio_venta_usd = form.cleaned_data['precio_venta_usd']
        facturacion.tipo_cambio = form.cleaned_data['tipo_cambio']
        facturacion.anho_venta = form.cleaned_data['anho_venta']
        facturacion.cliente = self.object
        facturacion.produccion = produccion
        facturacion.save()
        
        return super(ClientesCreate, self).form_valid(form)
    
    def form_invalid(self,form):
        print(form.errors)
        return super(ClientesCreate, self).form_invalid(form)
    
