from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import BienesCreate, ClientesCreate, produccion_get_data

urlpatterns = [
    url(r'^registro$', login_required(BienesCreate.as_view()) ,name="bienes_registro_create"),
    url(r'^registro_cliente$', login_required(ClientesCreate.as_view()) ,name="cliente_registro_create"),
]

# Urls usadas para ajax
urlpatterns += [
    url(r'^ajax/produccion_data$', login_required(produccion_get_data) ,name="produccion_data"),
]