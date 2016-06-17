from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import SubUnidadEconomicaCreate

urlpatterns = [
    url(r'^registro', login_required(SubUnidadEconomicaCreate.as_view()) ,name="sub_unidad_create"),
]