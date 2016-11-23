from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import ServiciosGeneralesCreate, ServiciosClientesCreate, servicios_get_data, servicios_cliente_get_data

urlpatterns = [
    url(r'^registro$', login_required(ServiciosGeneralesCreate.as_view()) ,name="servicio_general_create"),
    url(r'^registro-cliente$', login_required(ServiciosClientesCreate.as_view()) ,name="servicio_cliente_create"),
]

# Urls usadas para ajax
urlpatterns += [
    url(r'^ajax/servicios-data$', login_required(servicios_get_data) ,name="servicios_data"),
    url(r'^ajax/servicios-cliente-data$', login_required(servicios_cliente_get_data) ,name="servicios_cliente_data"),
]