"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.insumo_proveedores.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo de insumos y proveedores
# @author Hugo Ramirez (hramirez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @date 14-09-2016
# @version 2.0

import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.apps import apps
from django import forms
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from base.constant import CREATE_MESSAGE
from base.models import Proveedor, AnhoRegistro, Pais
from unidad_economica.bienes_prod_comer.models import Producto
from .models import Insumo, InsumoProduccion, InsumoProveedor
from .forms import InsumoProveedorForm, InsumoForm

class InsumoCreate(SuccessMessageMixin,CreateView):
    """!
    Clase que registra los insumos

    @author Hugo Ramirez (hramirez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 14-09-2016
    @version 2.0.0
    """
    model = Insumo
    form_class = InsumoForm
    template_name = "insumos.proveedores.template.html"
    success_url = reverse_lazy('insumo_create')
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
        kwargs = super(InsumoCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def form_valid(self,form):
        """!
        Metodo que valida si el formulario es valido, en cuyo caso se procede a registrar los datos de los insumos
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 20-12-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        producto = Producto.objects.get(pk=form.cleaned_data['producto'])
        
        ## Se crea la instancia del año
        anho = AnhoRegistro.objects.get(pk=form.cleaned_data['anho'])
        
        ## Se crea y se guarda el modelo de insumo
       
        self.object = form.save(commit=False)
        self.object.nombre_insumo = form.cleaned_data['nombre_insumo']
        self.object.producto = producto
        self.object.save()
        
        ## Se crea y se guarda el modelo de producción del insumo
        produccion = InsumoProduccion()
        produccion.especificacion_tecnica = form.cleaned_data['especificacion_tecnica']
        produccion.marca = form.cleaned_data['marca']
        produccion.relacion = form.cleaned_data['relacion']
        produccion.numero_proveedor = form.cleaned_data['numero_proveedor']
        produccion.anho_registro = anho
        produccion.insumo = self.object
        produccion.save()
        
        
        return super(InsumoCreate, self).form_valid(form)
    
    
def insumo_get_data(request):
    """!
    Metodo que extrae los datos de los insumos relacionados con la subunidad y la muestra en una url ajax como json

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 20-12-2016
    @param request <b>{object}</b> Recibe la peticion
    @return Retorna el json con las subunidades que consiguió
    """
    datos = {'data':[]}
    # Recibe por get el id de subunidad
    subid = request.GET.get('subunidad_id', None)
    if(subid):
        for ins in InsumoProduccion.objects.filter(insumo__producto__subunidad_id=subid,insumo__producto__subunidad__unidad_economica__user_id=request.user.id).all():
            lista = []
            lista.append(ins.insumo.producto.nombre_producto)
            lista.append(ins.insumo.nombre_insumo)
            lista.append(ins.especificacion_tecnica)
            lista.append(ins.marca)
            lista.append(ins.relacion)
            lista.append(ins.numero_proveedor)
            datos['data'].append(lista)
        
        return JsonResponse(datos,safe=False)
    return JsonResponse("No se envío el id de la subunidad",safe=False)


class InsumoProveedorCreate(SuccessMessageMixin,CreateView):
    """!
    Clase que registra los proveedores

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-12-2016
    @version 2.0.0
    """
    model = InsumoProveedor
    form_class = InsumoProveedorForm
    template_name = "insumos.proveedores.template.html"
    success_url = reverse_lazy('proveedor_create')
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
        kwargs = super(InsumoProveedorCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def form_valid(self,form):
        """!
        Metodo que valida si el formulario es valido, en cuyo caso se procede a registrar los datos del proveedor
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 21-12-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        ## Se intancia el pais
        pais = Pais.objects.get(pk=form.cleaned_data['pais_origen'])
        
        ## Se instancia en insumo-produccion
        insumo_produccion = InsumoProduccion.objects.get(insumo_id=form.cleaned_data['insumo'],anho_registro=form.cleaned_data['anho'])
        
        ## Se crea la instancia del año
        anho = AnhoRegistro.objects.get(pk=insumo_produccion.anho_registro_id)
        
        if(form.cleaned_data['rif']):
            ## Se busca el cliente si ya existe
            proveedor = Proveedor.objects.filter(rif=form.cleaned_data['rif'])
            if proveedor:
                proveedor = proveedor.get()  
            else:
                ## Se crea y se guarda el modelo de cliente
                proveedor = Proveedor()
                proveedor.nombre = form.cleaned_data['nombre_proveedor']
                #Si es venezuela se toma en cuenta el rif
                if(pais.pk==1):
                    proveedor.rif = form.cleaned_data['rif']
                proveedor.pais = pais
                proveedor.save()
        else:
            proveedor = Proveedor()
            proveedor.nombre = form.cleaned_data['nombre_proveedor']
            proveedor.pais = pais
            proveedor.save()
        
        ## Se crea y se guarda el modelo de facturacion de insumo-proveedor
        self.object = form.save(commit=False)
        self.object.precio_compra_bs = form.cleaned_data['precio_compra_bs']
        self.object.precio_compra_usd = form.cleaned_data['precio_compra_usd']
        self.object.cantidad_comprada = form.cleaned_data['cantidad_comprada']
        self.object.unidad_de_medida = form.cleaned_data['unidad_de_medida']
        self.object.proveedor = proveedor
        self.object.insumo_produccion = insumo_produccion
        self.object.save()
        
        return super(InsumoProveedorCreate, self).form_valid(form)
    
    
def proveedor_get_data(request):
    """!
    Metodo que extrae los datos de los clientes relacionados con el proveedor y la muestra en una url ajax como json

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 21-12-2016
    @param request <b>{object}</b> Recibe la peticion
    @return Retorna el json con las subunidades que consiguió
    """
    datos = {'data':[]}
    # Recibe por get el id del insumo
    insid = request.GET.get('insumo_id', None)
    if(insid):
        for insumo in InsumoProveedor.objects.filter(insumo_produccion__insumo_id=insid).all():
            lista = []
            lista.append(insumo.insumo_produccion.insumo.producto.nombre_producto)
            lista.append(insumo.insumo_produccion.insumo.nombre_insumo)
            lista.append(insumo.proveedor.nombre)
            lista.append(insumo.proveedor.pais.nombre)
            lista.append(insumo.proveedor.rif)
            lista.append(insumo.precio_compra_bs)
            lista.append(insumo.precio_compra_usd)
            lista.append(insumo.cantidad_comprada)
            lista.append(insumo.unidad_de_medida)
            datos['data'].append(lista)
        
        return JsonResponse(datos,safe=False)
    return JsonResponse("No se envío el id del servicio",safe=False)
