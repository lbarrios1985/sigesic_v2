from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import BienesGeneralesCreate, BienesCreate, ClientesCreate

urlpatterns = [
    url(r'^registro$', login_required(BienesGeneralesCreate.as_view()) ,name="bienes_generales_create"),
    url(r'^registro_bien$', login_required(BienesCreate.as_view()) ,name="bienes_registro_create"),
    url(r'^registro_cliente$', login_required(ClientesCreate.as_view()) ,name="cliente_registro_create"),
]
