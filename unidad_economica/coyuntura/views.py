from django.shortcuts import render, redirect
from django.http import JsonResponse
#from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from .forms import ProduccionForm
from unidad_economica.bienes_prod_comer.models import Producto, SubUnidadEconomica
from .models import Anho, Periodicidad, Produccion
from base.models import Cliente
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
        @date 14-07-2016
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

        anho= Anho()
        anho.anho= form.cleaned_data['anho']
        anho.save()

        periodicidad= Periodicidad()
        periodicidad.descripcion= form.cleaned_data['periodicidad']

        periodicidad.mes= form.cleaned_data['mes']
        periodicidad.trimestre= form.cleaned_data['trimestre']

        periodicidad.anho= anho
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
    @date 05-10-2016
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
            print(prod.producto.nombre_producto)
            print(prod.producto.especificacion_tecnica)
            print(prod.producto.marca)
            print(prod.cantidad_produccion)
            print(prod.numero_clientes)

            lista.append(prod.cantidad_produccion)
            lista.append(str(dic_um.get(prod.unidad_medida)))
            lista.append(prod.numero_clientes)
            datos['data'].append(lista)
        
        return JsonResponse(datos,safe=False)
    return JsonResponse("No se envío el id de la subunidad",safe=False)

