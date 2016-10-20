from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    url(r'^registro', login_required(ServiciosGeneralesCreate.as_view()) ,name="servicio_general_create"),
]

# Urls usadas para ajax
urlpatterns += [
    url(r'^ajax/servicios-data$', login_required(servicios_get_data) ,name="servicios_data"),
]