from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import ProduccionCreate, produccion_get_data

urlpatterns = [
    url(r'^registro$', login_required(ProduccionCreate.as_view()), name='coyuntura_registro_create'),
    #url(r'^registro_cliente$', login_required(CoyunturaCliente.as_view()) ,name="cliente_registro_create"),
]

# Urls usadas para ajax
urlpatterns += [
    url(r'^ajax/coyuntura-produccion-data$', login_required(produccion_get_data) ,name="coyuntura_produccion_data"),
    #url(r'^ajax/clientes-data$', login_required(clientes_get_data) ,name="clientes_data"),
]
