from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from .forms import ProduccionForm, ClientesForm
from unidad_economica.bienes_prod_comer.models import Producto
from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica
from .models import Periodicidad, Produccion, Clientes
from base.models import Cliente, Pais
from base.constant import CREATE_MESSAGE, UNIDAD_MEDIDA

# Create your views here.

class ProduccionCreate(SuccessMessageMixin, CreateView):
    model= Produccion
    form_class = ProduccionForm
    template_name = "coyuntura.template.html"
    success_url = reverse_lazy('coyuntura_registro_create')
    success_message = CREATE_MESSAGE

    def get_form_kwargs(self):
        """!
        Metodo que permite guardar el username en los kwargs
    
        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 22-12-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el kwargs con el username
        """
        kwargs = super(ProduccionCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self,form):
        """!
        Si el formulario es válido, se procede a registrar los datos de la Producción
    
        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 22-12-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado"""

        periodicidad= Periodicidad()
        periodicidad.periodo= form.cleaned_data['periodo']

        periodicidad.mes= form.cleaned_data['mes']
        periodicidad.trimestre= form.cleaned_data['trimestre']

        periodicidad.anho= form.cleaned_data['anho']
        periodicidad.save()

        sub_unidad_economica= SubUnidadEconomica.objects.get(pk=form.cleaned_data['sub_unidad_economica'])
        producto= Producto.objects.get(pk=form.cleaned_data['producto'])

        self.object= form.save(commit=False)
        self.object.cantidad_produccion= form.cleaned_data['cantidad_produccion']
        self.object.unidad_medida= form.cleaned_data['unidad_medida']
        self.object.numero_clientes= form.cleaned_data['numero_clientes']
        self.object.cantidad_produccion= form.cleaned_data['cantidad_produccion']
        self.object.sub_unidad_economica= sub_unidad_economica
        self.object.producto= producto
        self.object.periodicidad= periodicidad
        self.object.save()

        return super(ProduccionCreate, self).form_valid(form)

    def form_invalid(self,form):
        print(form.errors)
        return super(ProduccionCreate, self).form_invalid(form)

def produccion_get_data(request):
    """!
    Metodo que extrae los datos de los bienes relacionados con la subunidad y la muestra en una url ajax como json

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 22-12-2016
    @param request <b>{object}</b> Recibe la peticion
    @return Retorna el json con las subunidades que consiguió
    """
    datos = {'data':[]}
    dic_um = dict(UNIDAD_MEDIDA)
    # Recibe por get el id de subunidad
    subid = request.GET.get('subunidad_id', None)
    if(subid):
        for prod in Produccion.objects.filter(producto__subunidad_id=subid,producto__subunidad__unidad_economica__user_id=request.user.id).all():
            lista = []
            lista.append(prod.producto.nombre_producto)
            lista.append(prod.producto.especificacion_tecnica)
            lista.append(prod.producto.marca)

            #en esta línea va el código arancelario MERCOSUR

            lista.append(prod.cantidad_produccion)
            lista.append(str(dic_um.get(prod.unidad_medida)))
            lista.append(prod.numero_clientes)
            datos['data'].append(lista)
        
        return JsonResponse(datos,safe=False)
    return JsonResponse("No se envío el id de la subunidad",safe=False)

class ClientesCreate(SuccessMessageMixin, CreateView):
    model= Clientes
    form_class = ClientesForm
    template_name = "coyuntura.template.html"
    success_url = reverse_lazy('clientes_registro_create')
    success_message = CREATE_MESSAGE

    def get_form_kwargs(self):
        """!
        Metodo que permite guardar el username en los kwargs
    
        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 22-12-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el kwargs con el username
        """
        kwargs = super(ClientesCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self,form):
        """!
        Metodo que valida si el formulario es valido, en cuyo caso se procede a registrar los datos del cliente
    
        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 10-01-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """

        produccion = Produccion.objects.filter(producto__subunidad_id=form.cleaned_data['sub_unidad_economica_cliente'],producto_id=form.cleaned_data['producto_cliente']).get()
        pais = Pais.objects.get(pk=form.cleaned_data['ubicacion_cliente'])
        producto = Producto.objects.get(pk=form.cleaned_data['producto_cliente'])
        
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
        self.object.cantidad_vendida = form.cleaned_data['cantidad_vendida']
        self.object.unidad_medida = form.cleaned_data['unidad_medida_cliente']
        self.object.precio_bs = form.cleaned_data['precio_bs']
        self.object.precio_usd = form.cleaned_data['precio_usd']
        self.object.cliente = cliente
        self.object.produccion = produccion
        self.object.save()
        
        return super(ClientesCreate, self).form_valid(form)
    
    def form_invalid(self,form):
        return super(ClientesCreate, self).form_invalid(form)

def clientes_get_data(request):
    """!
    Metodo que extrae los datos de los clientes relacionados con el producto y la muestra en una url ajax como json

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 05-10-2016
    @param request <b>{object}</b> Recibe la peticion
    @return Retorna el json con las subunidades que consiguió
    """
    datos = {'data':[]}
    dic_um = dict(UNIDAD_MEDIDA)
    # Recibe por get el id del producto
    prodid = request.GET.get('producto_id', None)
    if(prodid):
        for clientes in Clientes.objects.filter(produccion__producto_id=prodid).all():
            lista = []
            lista.append(clientes.produccion.producto.nombre_producto)
            lista.append(clientes.cliente.nombre)
            lista.append(clientes.cliente.pais.nombre)
            lista.append(clientes.cliente.rif)
            lista.append(clientes.cantidad_vendida)
            lista.append(str(dic_um.get(clientes.unidad_medida)))
            lista.append(clientes.precio_bs)
            lista.append(clientes.precio_usd)
            datos['data'].append(lista)
        
        return JsonResponse(datos,safe=False)
    return JsonResponse("No se envío el id del producto",safe=False)

