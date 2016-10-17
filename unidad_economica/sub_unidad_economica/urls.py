from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import SubUnidadEconomicaCreate, subunidad_get_data

urlpatterns = [
    url(r'^registro', login_required(SubUnidadEconomicaCreate.as_view()) ,name="sub_unidad_create"),
]

# Ajax urls
urlpatterns += [
    url(r'^ajax/get_data$', login_required(subunidad_get_data) ,name="subunidad_data"),
]