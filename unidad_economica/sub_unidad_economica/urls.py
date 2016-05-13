from django.conf.urls import url
from .views import SubUnidadEconomicaCreate

urlpatterns = [
    url(r'^registro', SubUnidadEconomicaCreate.as_view() ,name="sub_unidad_create"),
]